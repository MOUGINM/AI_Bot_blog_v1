from flask import Flask, jsonify, request, render_template
import openai
import key
app = Flask(__name__)

# Remplace par tes clés API
openai.api_key = key.openai_key

def generate_blog_content():
    try:
        prompt = ("Crée un court article de blog sur la technologie. Commence par un titre accrocheur et original, suivi de quelques lignes de contenu.En français\n\n"
                  "Inclut peu d'émojis,peu d'hashtags et des informations intéressantes pour attirer l'attention !Place des mots en gras.\n\n"
                  "Ne dépasse pas une 150 mots environ.\n")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )

        content = response.choices[0].message["content"]
        title, article = content.split('\n', 1)
        return title.strip(), article.strip()
    except Exception as e:
        return "Erreur de Génération", str(e)

@app.route('/generate_blog', methods=['GET'])
def generate_blog():
    contents = []
    for _ in range(3):  # Générer 3 articles
        title, article = generate_blog_content()
        contents.append({"type": "blog", "title": title, "content": article})
    return jsonify(contents)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
