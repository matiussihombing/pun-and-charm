from flask import Flask, request, jsonify, send_from_directory
import database

app = Flask(__name__, static_url_path='', static_folder='.')

# Initial Data for Seeding
INITIAL_DATA = {
    'en': {
        'jokes': [
            "I'm afraid for the calendar. Its days are numbered.",
            "My wife said I should do lunges to stay in shape. That would be a big step forward.",
            "Why do fathers take an extra pair of socks when they go golfing? In case they get a hole in one!",
            "Singing in the shower is fun until you get soap in your mouth. Then it's a soap opera.",
            "What do a tick and the Eiffel Tower have in one? They're both Paris sites.",
            "What do you call a fish wearing a bowtie? Sofishticated.",
            "How do you follow Will Smith in the snow? You follow the fresh prints.",
            "If April showers bring May flowers, what do May flowers bring? Pilgrims.",
            "I thought the dryer was shrinking my clothes. Turns out it was the refrigerator all along.",
            "How does dry skin affect you at work? You don’t have any elbow grease to put into it.",
            "What do you call a factory that makes okay products? A satisfactory.",
            "Dear Math, grow up and solve your own problems.",
            "What did the janitor say when he jumped out of the closet? Supplies!",
            "Have you heard about the chocolate record player? It sounds pretty sweet.",
            "What did the ocean say to the beach? Nothing, it just waved.",
            "Why do seagulls fly over the ocean? Because if they flew over the bay, we'd call them bagels.",
            "I only know 25 letters of the alphabet. I don't know y.",
            "How does the moon cut his hair? Eclipse it.",
            "What did one wall say to the other? I'll meet you at the corner.",
            "I used to play piano by ear, but now I use my hands.",
            "Why don't skeletons fight each other? They don't have the guts.",
            "What do you call a fake noodle? An impasta.",
            "Why did the scarecrow win an award? Because he was outstanding in his field.",
            "I would avoid the sushi if I was you. It’s a little fishy."
        ],
        'pickup': [
            "Are you a magician? Because whenever I look at you, everyone else disappears.",
            "Do you have a map? I keep getting lost in your eyes.",
            "Is your name Google? Because you have everything I've been searching for.",
            "Are you a time traveler? Because I see you in my future.",
            "Do you have a name, or can I call you mine?",
            "If you were a vegetable, you'd be a cute-cumber.",
            "Do you believe in love at first sight—or should I walk by again?",
            "Is it hot in here or is it just you?",
            "I'm not a photographer, but I can picture us together.",
            "Are you a parking ticket? Because you've got FINE written all over you.",
            "Did it hurt? When you fell from heaven?",
            "Can I follow you where you're going? Because my parents always told me to follow my dreams.",
            "Is your dad a boxer? Because damn, you're a knockout!",
            "If I could rearrange the alphabet, I’d put ‘U’ and ‘I’ together.",
            "Are you French? Because Eiffel for you.",
            "Do you have a sunburn, or are you always this hot?",
            "I must be a snowflake, because I've fallen for you.",
            "Are you made of copper and tellurium? Because you're CuTe.",
            "I was wondering if you had an extra heart. The doctor took mine.",
            "If you were a fruit, you'd be a fineapple.",
            "Are you a camera? Because every time I look at you, I smile.",
            "Do you have a Band-Aid? I just scraped my knee falling for you.",
            "Is there an airport nearby or is it my heart taking off?",
            "I’m learning about important dates in history. Wanna be one of them?"
        ]
    },
    'id': {
        'jokes': [
            "Kenapa zombie kalau nyerang bareng-bareng? Karena kalau sendiri namanya zomblo.",
            "Sayur apa yang bisa nyanyi? Kolplay.",
            "Gendang apa yang nggak bisa dipukul? Gendang telinga.",
            "Ayam apa yang paling besar? Ayam semesta.",
            "Ikan apa yang suka berhenti? Ikan pause.",
            "Kucing apa yang romantis? Kucingta padamu.",
            "Buah apa yang durhaka? Melon kundang.",
            "Kenapa pohon kelapa di depan rumah harus ditebang? Soalnya kalau dicabut berat.",
            "Hewan apa yang paling hening? Semut dalam tapa.",
            "Apa bedanya soto sama coto? Kalau soto dari daging sapi, kalau coto dari daging capi.",
            "Kenapa anak kucing dan anak anjing suka berantem? Namanya juga anak-anak.",
            "Penyanyi luar negeri yang suka bersepeda? Selena Gowes.",
            "Ada nggak buah yang berbahaya? Ada, buahaya.",
            "Kenapa air mata warnanya bening? Kalau ijo namanya air matcha.",
            "Sapi, sapi apa yang nempel di dinding? Stiker sapi.",
            "Kenapa nyamuk bunyinya nging nging? Karena dia menghisap darah, bukan menghisap rokok.",
            "Benda apa yang kalau dipotong malah makin tinggi? Celana panjang.",
            "Kenapa Superman bajunya ada huruf S? Kalau M atau XL kegedean.",
            "Apa bahasa Cinanya aneka macam sayur? Cap Cay.",
            "Kenapa dalang bawa keris pas pertunjukan wayang? Kalau bawa kompor, istrinya nggak bisa masak."
        ],
        'pickup': [
            "Kamu punya peta nggak? Aku tersesat di matamu.",
            "Bapak kamu maling ya? Karena kamu telah mencuri hatiku.",
            "Kamu tahu bedanya kamu sama jam 12 siang? Kalau jam 12 siang itu kesiangan, kalau kamu kesayangan.",
            "Cuka apa yang manis? Cuka sama kamu.",
            "Minyak apa yang bikin mabuk? Minyaksikan senyummu.",
            "Kamu tahu nggak kenapa aku suka apel? Soalnya aku mau apel ke rumahmu.",
            "Tiang apa yang enak? Tiang-tiang mikirin kamu.",
            "Kuda apa yang bikin seneng? Kudapat pacar sepertimu.",
            "Kamu itu kayak lempeng bumi ya, bisa menggoncangkan hatiku.",
            "Apa bedanya monas sama kamu? Monas milik negara, kalau kamu milik aku.",
            "Cecak apa yang bisa bikin mati? Cecak napas liat senyummu.",
            "Kamu kenal mendung nggak? Mendung itu kalau nggak ada kamu.",
            "Tahu nggak kenapa menara pisa miring? Soalnya ketarik sama senyummu.",
            "Jalan mundur nabrak tukang jamu, aku nggak bisa tidur gara-gara mikirin kamu.",
            "Kamu tahu nggak, aku itu pro banget lho. Pro-tektif sama kamu.",
            "Mobil apa yang bikin galau? Mobilang sayang tapi takut ditolak.",
            "Awan apa yang bikin seneng? Awanna be with you.",
            "Kipas apa yang ditunggu-tunggu cewek? Kipastian.",
            "Malam apa yang paling indah? Malamar kamu.",
            "Setan apa yang paling romantis? Setangkai bunga mawar untukmu."
        ]
    }
}

# Initialize DB
database.init_db()
database.seed_data(INITIAL_DATA)

@app.route('/')
def hello():
    return send_from_directory('.', 'index.html')

@app.route('/admin')
def admin_page():
    return send_from_directory('.', 'admin.html')

@app.route('/manifest.json')
def manifest():
    return send_from_directory('.', 'manifest.json')

@app.route('/sw.js')
def service_worker():
    return send_from_directory('.', 'sw.js')

@app.route('/api/random', methods=['GET'])
def get_random():
    type_ = request.args.get('type', 'jokes')
    lang = request.args.get('lang', 'en')
    exclude = request.args.get('exclude', '')
    
    exclude_ids = []
    if exclude:
        try:
            exclude_ids = [int(x) for x in exclude.split(',')]
        except ValueError:
            pass
            
    content = database.get_random_content(type_, lang, exclude_ids)
    if content:
        return jsonify(content)
    return jsonify({"error": "No content found"}), 404

@app.route('/api/rate', methods=['POST'])
def rate_content():
    data = request.get_json()
    if not data or 'id' not in data or 'score' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    success = database.add_rating(data['id'], int(data['score']))
    if success:
        return jsonify({"message": "Rating added"})
    return jsonify({"error": "Failed to add rating"}), 400

@app.route('/api/submit', methods=['POST'])
def submit_content():
    data = request.get_json()
    if not data or 'type' not in data or 'lang' not in data or 'text' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    success = database.submit_content(data['type'], data['lang'], data['text'])
    if success:
        return jsonify({"message": "Submission received! Waiting for approval."})
    return jsonify({"error": "Failed to submit"}), 400

# Admin Routes
ADMIN_PASSWORD = "supersecretpassword" # Simple protection

def check_auth(req):
    auth = req.headers.get('Authorization')
    return auth == ADMIN_PASSWORD

@app.route('/api/admin/pending', methods=['GET'])
def get_pending():
    if not check_auth(request):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(database.get_pending_content())

@app.route('/api/admin/approve', methods=['POST'])
def approve_content():
    if not check_auth(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    database.update_content_status(data['id'], 'approved')
    return jsonify({"message": "Approved"})

@app.route('/api/admin/reject', methods=['POST'])
def reject_content():
    if not check_auth(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    database.delete_content(data['id'])
    return jsonify({"message": "Rejected"})

if __name__ == '__main__':
    app.run(debug=True)
