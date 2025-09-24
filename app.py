from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 用於flash消息

# 記憶體資料結構模擬資料庫
patients = [
    {
        'id': str(uuid.uuid4()),
        'name': '張小明',
        'age': 35,
        'gender': '男',
        'diagnosis': '感冒',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    {
        'id': str(uuid.uuid4()),
        'name': '李美麗',
        'age': 28,
        'gender': '女',
        'diagnosis': '頭痛',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    {
        'id': str(uuid.uuid4()),
        'name': '王大華',
        'age': 42,
        'gender': '男',
        'diagnosis': '高血壓',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
]

@app.route('/')
def index():
    """病人列表頁（首頁）"""
    return render_template('index.html', patients=patients)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    """新增病人頁"""
    if request.method == 'POST':
        # 獲取表單資料
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        gender = request.form.get('gender', '')
        diagnosis = request.form.get('diagnosis', '').strip()
        
        # 驗證必填欄位
        if not name or not age or not gender:
            flash('姓名、年齡和性別為必填欄位！', 'error')
            return render_template('add_patient.html')
        
        # 驗證年齡為數字
        try:
            age = int(age)
            if age <= 0 or age > 150:
                flash('年齡必須在1-150之間！', 'error')
                return render_template('add_patient.html')
        except ValueError:
            flash('年齡必須是數字！', 'error')
            return render_template('add_patient.html')
        
        # 建立新病人資料
        new_patient = {
            'id': str(uuid.uuid4()),
            'name': name,
            'age': age,
            'gender': gender,
            'diagnosis': diagnosis,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 加入病人清單
        patients.append(new_patient)
        flash(f'成功新增病人：{name}', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_patient.html')

@app.route('/patient/<patient_id>')
def patient_detail(patient_id):
    """病人詳細頁"""
    # 尋找病人
    patient = None
    for p in patients:
        if p['id'] == patient_id:
            patient = p
            break
    
    if not patient:
        flash('找不到指定的病人資料！', 'error')
        return render_template('error.html', message='病人不存在')
    
    return render_template('patient_detail.html', patient=patient)

@app.errorhandler(404)
def not_found(error):
    """404錯誤處理"""
    return render_template('error.html', message='頁面不存在'), 404

@app.errorhandler(500)
def internal_error(error):
    """500錯誤處理"""
    return render_template('error.html', message='伺服器內部錯誤'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
