from flask import Flask, render_template, request
import os, json, re

app = Flask(__name__)

def load_options():
    options_path = "options"
    options_data = {}
    for filename in os.listdir(options_path):
        if filename.endswith(".json"):
            with open(os.path.join(options_path, filename), 'r') as json_file:
                # Charge le contenu du fichier JSON
                data = json.load(json_file)
            # Assume que le nom de l'option est la clé principale dans le fichier JSON
            option_name = list(data.keys())[0]
            # Stocke la liste des options disponibles pour cette option dans le dictionnaire
            options_data[option_name] = data[option_name]
    return options_data

@app.route('/')
def form():
    options_data = load_options()

    tab_categories = {
        "Modele": ["gender", "ethnic", "haircut", "hair_color", "eyes_color", "skin_detail", "outfitt", "accessories"],
        "Camera": ["camera", "camera_position", "lens", "aperture", "film_effects"],
        "Environment": ["lighting", "background"],
        "Poses": ["body_position", "facial_expression", "gaze_expression"],
        "Framing": ["frame", "medium"],
        "Effects" : ["effects"]
    }

    return render_template('form.html', options=options_data, tab_categories=tab_categories)

@app.route('/generate', methods=['POST'])
def generate():
    subject = request.form['subject']
    
    # Initialisation du dictionnaire pour stocker les options avec leurs poids
    prompt_parts = {}
    
    options = load_options()

    for option in ['effects', 'accessories']:
        selected_items = request.form.getlist(option)
        cleaned_items = [re.sub(r'\s*\(.*?\)\s*', '', item).strip() for item in selected_items]
        prompt_parts[option] = ', '.join(cleaned_items)

        weight = request.form.get(f"{option}_weight", '1')  # Récupérer le poids spécifique à l'option
    
    for option in options:

        if option not in ['effects', 'accessories']:
        
            option_value = request.form.get(option, '')
            weight = request.form.get(f"{option}_weight", '1')  # Récupérer le poids spécifique à l'option

            if option_value == "Other":
                option_value = request.form.get(f"{option}_other")
            
            if option_value and "(" in option_value:
                option_value = option_value.split(" (")[0]
    
            if option_value:
                # Inclure le poids dans le prompt uniquement s'il diffère de 1
                formatted_option = f"{option_value}" if weight == '1' else f"({option_value}: {weight})"
                prompt_parts[option] = formatted_option

    # Construction du prompt complet avec les poids spécifiques
    prompt = f"{prompt_parts.get('frame', '')} \
        {prompt_parts.get('medium', '')} \
        of a {prompt_parts.get('ethnic', '')} \
        {subject} \
        {prompt_parts.get('gender', '')}, \
        {prompt_parts.get('camera_position', '')}, \
        {prompt_parts.get('eyes_color', '')}, \
        {prompt_parts.get('haircut', '')}, \
        {prompt_parts.get('hair_color', '')}, \
        {prompt_parts.get('skin_detail', '')}, \
        {prompt_parts.get('outfitt', '')}, \
        {prompt_parts.get('accessories', '')}, \
        {prompt_parts.get('facial_expression', '')}, \
        {prompt_parts.get('gaze_expression', '')}, \
        {prompt_parts.get('body_position', '')}, \
        {prompt_parts.get('background', '')}, \
        {prompt_parts.get('lighting', '')}, \
        {prompt_parts.get('camera', '')}, \
        {prompt_parts.get('film_effects', '')}, \
        {prompt_parts.get('lens', '')}, \
        {prompt_parts.get('aperture', '')}, \
        {prompt_parts.get('effects', '')} \
        "
    prompt = ' '.join(prompt.split())  # Nettoyage des espaces supplémentaires
    
    return render_template('result.html', prompt=prompt)


if __name__ == '__main__':
    app.run(debug=True)
