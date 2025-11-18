from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import calendar

app = Flask(__name__)

# Import dari file lain (sesuaikan dengan struktur project kamu)
from db import get_db_connection

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Hitung total pemasukan dan pengeluaran
    cursor.execute("SELECT COALESCE(SUM(jumlah), 0) FROM transaksi WHERE jenis='masuk'")
    total_pemasukan = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COALESCE(SUM(jumlah), 0) FROM transaksi WHERE jenis='keluar'")
    total_pengeluaran = cursor.fetchone()[0] or 0
    
    saldo = total_pemasukan - total_pengeluaran
    
    # Data untuk chart kategori (pengeluaran per kategori/deskripsi)
    cursor.execute("""
        SELECT deskripsi, SUM(jumlah) as total 
        FROM transaksi 
        WHERE jenis='keluar' 
        GROUP BY deskripsi
        ORDER BY total DESC
    """)
    kategori_data = cursor.fetchall()
    kategori_labels = [row[0] for row in kategori_data]
    kategori_values = [row[1] for row in kategori_data]
    
    # Data untuk trend bulanan (6 bulan terakhir) - MySQL syntax
    cursor.execute("""
        SELECT DATE_FORMAT(tanggal, '%Y-%m') as bulan, 
               jenis, 
               SUM(jumlah) as total
        FROM transaksi 
        WHERE tanggal >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
        GROUP BY bulan, jenis
        ORDER BY bulan
    """)
    trend_data = cursor.fetchall()
    
    # Proses data trend
    bulan_dict = {}
    for row in trend_data:
        bulan = row[0] if row[0] else datetime.now().strftime('%Y-%m')
        jenis = row[1]
        total = row[2]
        
        if bulan not in bulan_dict:
            bulan_dict[bulan] = {'masuk': 0, 'keluar': 0}
        bulan_dict[bulan][jenis] = total
    
    bulan_labels = []
    pemasukan_bulanan = []
    pengeluaran_bulanan = []
    
    # Jika tidak ada data trend, gunakan bulan saat ini
    if not bulan_dict:
        bulan_dict[datetime.now().strftime('%Y-%m')] = {'masuk': 0, 'keluar': 0}
    
    for bulan in sorted(bulan_dict.keys()):
        # Format bulan dari YYYY-MM ke nama bulan
        try:
            year, month = bulan.split('-')
            month_name = calendar.month_abbr[int(month)]
            bulan_labels.append(f"{month_name} {year}")
        except:
            bulan_labels.append(bulan)
        
        pemasukan_bulanan.append(bulan_dict[bulan]['masuk'])
        pengeluaran_bulanan.append(bulan_dict[bulan]['keluar'])
    
    # Transaksi terbaru (5 terakhir)
    cursor.execute("""
        SELECT DATE_FORMAT(tanggal, '%Y-%m-%d') as tanggal, deskripsi, jenis, jumlah 
        FROM transaksi 
        ORDER BY tanggal DESC, id DESC 
        LIMIT 5
    """)
    transaksi_terbaru = []
    for row in cursor.fetchall():
        transaksi_terbaru.append({
            'tanggal': row[0],
            'kategori': row[1],  # deskripsi dijadikan kategori
            'jenis': 'Pemasukan' if row[2] == 'masuk' else 'Pengeluaran',
            'jumlah': row[3]
        })
    
    conn.close()
    
    # Data untuk chart
    chart_data = {
        'total_pemasukan': float(total_pemasukan),
        'total_pengeluaran': float(total_pengeluaran),
        'kategori_labels': kategori_labels,
        'kategori_values': [float(v) for v in kategori_values],
        'bulan_labels': bulan_labels,
        'pemasukan_bulanan': [float(v) for v in pemasukan_bulanan],
        'pengeluaran_bulanan': [float(v) for v in pengeluaran_bulanan]
    }
    
    return render_template('index.html',
                         total_pemasukan=total_pemasukan,
                         total_pengeluaran=total_pengeluaran,
                         saldo=saldo,
                         chart_data=chart_data,
                         transaksi_terbaru=transaksi_terbaru)

@app.route('/data')
def data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transaksi ORDER BY tanggal DESC, id DESC")
    transaksi = cursor.fetchall()
    conn.close()
    return render_template('data.html', transaksi=transaksi)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        jenis = request.form['jenis']
        deskripsi = request.form['deskripsi']
        jumlah = request.form['jumlah']
        tanggal = request.form.get('tanggal', datetime.now().strftime('%Y-%m-%d'))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transaksi (jenis, deskripsi, jumlah, tanggal) VALUES (%s, %s, %s, %s)",
            (jenis, deskripsi, jumlah, tanggal)
        )
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('tambah.html', today=today)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        jenis = request.form['jenis']
        deskripsi = request.form['deskripsi']
        jumlah = request.form['jumlah']
        tanggal = request.form['tanggal']
        
        cursor.execute(
            "UPDATE transaksi SET jenis=%s, deskripsi=%s, jumlah=%s, tanggal=%s WHERE id=%s",
            (jenis, deskripsi, jumlah, tanggal, id)
        )
        conn.commit()
        conn.close()
        
        return redirect(url_for('data'))
    
    cursor.execute("SELECT * FROM transaksi WHERE id=%s", (id,))
    transaksi = cursor.fetchone()
    conn.close()
    
    if not transaksi:
        return redirect(url_for('data'))
    
    return render_template('edit.html', transaksi=transaksi)

@app.route('/hapus/<int:id>', methods=['POST'])
def hapus(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transaksi WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('data'))

@app.route('/laporan')
def laporan():
    bulan = request.args.get('bulan', datetime.now().month, type=int)
    tahun = request.args.get('tahun', datetime.now().year, type=int)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM transaksi 
        WHERE MONTH(tanggal) = %s AND YEAR(tanggal) = %s
        ORDER BY tanggal DESC, id DESC
    """, (bulan, tahun))
    transaksi = cursor.fetchall()
    
    cursor.execute("""
        SELECT COALESCE(SUM(jumlah), 0) FROM transaksi 
        WHERE jenis='masuk' AND MONTH(tanggal) = %s AND YEAR(tanggal) = %s
    """, (bulan, tahun))
    total_pemasukan = cursor.fetchone()[0] or 0
    
    cursor.execute("""
        SELECT COALESCE(SUM(jumlah), 0) FROM transaksi 
        WHERE jenis='keluar' AND MONTH(tanggal) = %s AND YEAR(tanggal) = %s
    """, (bulan, tahun))
    total_pengeluaran = cursor.fetchone()[0] or 0
    
    saldo = total_pemasukan - total_pengeluaran
    
    cursor.execute("""
        SELECT deskripsi, SUM(jumlah) as total, COUNT(*) as jumlah_transaksi
        FROM transaksi 
        WHERE jenis='keluar' AND MONTH(tanggal) = %s AND YEAR(tanggal) = %s
        GROUP BY deskripsi
        ORDER BY total DESC
    """, (bulan, tahun))
    pengeluaran_per_kategori = cursor.fetchall()
    
    cursor.execute("""
        SELECT deskripsi, SUM(jumlah) as total, COUNT(*) as jumlah_transaksi
        FROM transaksi 
        WHERE jenis='masuk' AND MONTH(tanggal) = %s AND YEAR(tanggal) = %s
        GROUP BY deskripsi
        ORDER BY total DESC
    """, (bulan, tahun))
    pemasukan_per_kategori = cursor.fetchall()
    
    cursor.execute("SELECT DISTINCT YEAR(tanggal) as tahun FROM transaksi ORDER BY tahun DESC")
    tahun_list = [row[0] for row in cursor.fetchall()]
    if not tahun_list:
        tahun_list = [datetime.now().year]
    
    conn.close()
    
    nama_bulan = [
        'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
        'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
    ]
    
    return render_template('laporan.html',
                         bulan=bulan,
                         tahun=tahun,
                         nama_bulan=nama_bulan,
                         tahun_list=tahun_list,
                         transaksi=transaksi,
                         total_pemasukan=total_pemasukan,
                         total_pengeluaran=total_pengeluaran,
                         saldo=saldo,
                         pengeluaran_per_kategori=pengeluaran_per_kategori,
                         pemasukan_per_kategori=pemasukan_per_kategori)

@app.route('/budget', methods=['GET'])
def budget():
    bulan = request.args.get('bulan', datetime.now().month, type=int)
    tahun = request.args.get('tahun', datetime.now().year, type=int)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT deskripsi FROM transaksi WHERE jenis='keluar' ORDER BY deskripsi")
    kategori_list = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("""
        SELECT kategori, jumlah_budget 
        FROM budget 
        WHERE bulan=%s AND tahun=%s
    """, (bulan, tahun))
    budget_data = {row[0]: row[1] for row in cursor.fetchall()}
    
    cursor.execute("""
        SELECT deskripsi, SUM(jumlah) as total
        FROM transaksi 
        WHERE jenis='keluar' AND MONTH(tanggal)=%s AND YEAR(tanggal)=%s
        GROUP BY deskripsi
    """, (bulan, tahun))
    actual_data = {row[0]: row[1] for row in cursor.fetchall()}
    
    budget_summary = []
    for kategori in kategori_list:
        budget_amount = float(budget_data.get(kategori, 0))
        actual_amount = float(actual_data.get(kategori, 0))
        
        if budget_amount > 0:
            percentage = (actual_amount / budget_amount * 100)
            status = 'danger' if percentage > 100 else ('warning' if percentage > 80 else 'success')
        else:
            percentage = 0
            status = 'secondary'
        
        budget_summary.append({
            'kategori': kategori,
            'budget': budget_amount,
            'actual': actual_amount,
            'sisa': budget_amount - actual_amount,
            'percentage': min(percentage, 100),
            'percentage_full': percentage,
            'status': status
        })
    
    budget_summary.sort(key=lambda x: x['actual'], reverse=True)
    
    total_budget = sum(item['budget'] for item in budget_summary)
    total_actual = sum(item['actual'] for item in budget_summary)
    
    cursor.execute("SELECT DISTINCT YEAR(tanggal) as tahun FROM transaksi ORDER BY tahun DESC")
    tahun_list = [row[0] for row in cursor.fetchall()]
    if not tahun_list:
        tahun_list = [datetime.now().year]
    
    conn.close()
    
    nama_bulan = [
        'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
        'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
    ]
    
    return render_template('budget.html',
                         bulan=bulan,
                         tahun=tahun,
                         nama_bulan=nama_bulan,
                         tahun_list=tahun_list,
                         budget_summary=budget_summary,
                         total_budget=total_budget,
                         total_actual=total_actual,
                         kategori_list=kategori_list)

@app.route('/budget/set', methods=['POST'])
def set_budget():
    kategori = request.form['kategori']
    bulan = int(request.form['bulan'])
    tahun = int(request.form['tahun'])
    jumlah = float(request.form['jumlah'])
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO budget (kategori, bulan, tahun, jumlah_budget) 
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE jumlah_budget=%s
    """, (kategori, bulan, tahun, jumlah, jumlah))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('budget', bulan=bulan, tahun=tahun))

@app.route('/budget/delete/<kategori>/<int:bulan>/<int:tahun>', methods=['POST'])
def delete_budget(kategori, bulan, tahun):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM budget WHERE kategori=%s AND bulan=%s AND tahun=%s", 
                  (kategori, bulan, tahun))
    conn.commit()
    conn.close()
    
    return redirect(url_for('budget', bulan=bulan, tahun=tahun))

if __name__ == '__main__':
    app.run(debug=True)