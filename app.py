import os
import pyKVFinder
import pandas as pd
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'pdb'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure upload and output directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_pdb_file(filepath, probe_out, volume_cutoff):
    """Process PDB file with pyKVFinder."""
    # Run pyKVFinder workflow
    results = pyKVFinder.run_workflow(
        filepath, 
        probe_out=probe_out, 
        volume_cutoff=volume_cutoff, 
        include_depth=True, 
        include_hydropathy=True, 
        ignore_backbone=True
    )
    
    # Prepare output files
    filename = os.path.splitext(os.path.basename(filepath))[0]
    results_toml = os.path.join(OUTPUT_FOLDER, f'results_{filename}.toml')
    output_pdb = os.path.join(OUTPUT_FOLDER, f'output_{filename}.pdb')
    histograms_pdf = os.path.join(OUTPUT_FOLDER, f'histograms_{filename}.pdf')
    excel_file = os.path.join(OUTPUT_FOLDER, f'pocket_results_{filename}.xlsx')
    cavities_pdb = os.path.join(OUTPUT_FOLDER, f'cavities_{filename}.pdb')
    
    # Export results
    results.export_all(
        fn=results_toml, 
        output=output_pdb, 
        include_frequencies_pdf=True, 
        pdf=histograms_pdf
    )
    
    # Extract cavities information
    cavities = results.cavities
    areas = results.area
    volumes = results.volume
    max_depth = results.max_depth
    avg_depth = results.avg_depth
    avg_hydropathy = results.avg_hydropathy
    
    # Prepare pocket results DataFrame
    pocket_results = []
    for cavity, area in areas.items():
        pocket_results.append({
            'Cavity': cavity, 
            'Volume': volumes.get(cavity),
            'Area': area, 
            'Max_depth': max_depth.get(cavity),
            'Avg_depth': avg_depth.get(cavity), 
            'Avg_hydropathy': avg_hydropathy.get(cavity)
        })
    
    # Convert to DataFrame and save
    pockets_df = pd.DataFrame(pocket_results)
    pockets_df.to_excel(excel_file, index=False)
    
    # Write cavities PDB
    pyKVFinder.write_results(
        results_toml, 
        input=filepath, 
        volume=volumes, 
        area=areas, 
        ligand=None, 
        output=cavities_pdb
    )
    
    return {
        'results_toml': results_toml,
        'output_pdb': output_pdb,
        'histograms_pdf': histograms_pdf,
        'excel_file': excel_file,
        'cavities_pdb': cavities_pdb
    }

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if file is present
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')
        
        file = request.files['file']
        
        # Check if filename is empty
        if file.filename == '':
            return render_template('index.html', error='No selected file')
        
        # Check if file is allowed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Get parameters from form
            probe_out = float(request.form.get('probe_out', 8.0))
            volume_cutoff = float(request.form.get('volume_cutoff', 50.0))
            
            # Process file
            try:
                results = process_pdb_file(filepath, probe_out, volume_cutoff)
                return render_template('result.html', results=results)
            except Exception as e:
                return render_template('index.html', error=str(e))
        
        return render_template('index.html', error='Invalid file type')
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8008)
