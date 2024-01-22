from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data['query']
    response = f"사용자가 검색한 내용은 {query}입니다."
    return jsonify({'result': response})

if __name__ == '__main__':
    app.run(debug=True)