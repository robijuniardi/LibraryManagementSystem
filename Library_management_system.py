import connect_to_my_sql
import create_database
import mysql.connector 
from mysql.connector import Error
from datetime import date
from datetime import timedelta
today = date.today()


#Connection to mySQL and DB
nama_host = "localhost" # disesuaikan dengan nama komputer yang digunakan
user = "root" # disesuaikan dengan nama user yang digunakan untuk terkoneksi ke server
password = "     " # disesuaikan dengan password yang dibuat

# membuat koneksi ke server
myconn = mysql.connector.connect(host = nama_host, user = user, passwd = password, auth_plugin='mysql_native_password')

# membuat object cursor
mycursor = myconn.cursor()

# Membuat Database
mycursor.execute("CREATE DATABASE IF NOT EXISTS tugas_lms")

#koneksi ke database
db = "tugas_lms" 
mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
mycursor = mydb.cursor()


#Membuat tabel user
query_create_tabel_user = """
CREATE TABLE IF NOT EXISTS user(
  id_user INT AUTO_INCREMENT,
  user_name VARCHAR(40),
  tgl_lahir VARCHAR(10),
  pekerjaan VARCHAR(20),
  alamat VARCHAR(40),
  CONSTRAINT user primary key(id_user)
);
"""
mycursor.execute(query_create_tabel_user)
mydb.commit()

#insert database user
query_insert_data_user = """
INSERT INTO user VALUES
(1, 'Asraf', '1967-11-17', 'Guru', 'Jakarta'),
(2, 'Andi', '1961-05-11', 'karyawan swasta', 'Bogor'),
(3, 'Fitri', '1968-05-11', 'Penari', 'Depok'),
(4, 'Fawzi', '1971-06-25', 'Penyanyi', 'Tanggerang'),
(5, 'Dessy', '1980-02-05', 'Pembalap', 'Bekasi')
;
"""
mycursor.execute(query_insert_data_user)
mydb.commit()

#Membuat tabel buku
id_buku=1000
query_create_tabel_buku = """
CREATE TABLE IF NOT EXISTS buku(
  id_buku INT PRIMARY KEY AUTO_INCREMENT,
  nama_buku VARCHAR(40),
  kategory_buku VARCHAR(40),
  stock INT
);
"""
mycursor.execute(query_create_tabel_buku) # Mengeksekusi query
mydb.commit()

#insert database buku
query_insert_data_buku = """
INSERT INTO buku VALUES
(1001,'Fisika dasar', 'Pendidikan', 4),
(1002,'Kimia dasar', 'Pendidikan', 3),
(1003,'Laskar Pelangi', 'Novel Fiksi', 3),
(1004,'Halo Bandung', 'Sejarah', 4),
(1005,'Donald Bebek', 'Anak-anak', 2)
;
"""
mycursor.execute(query_insert_data_buku)
mydb.commit()

#Membuat tabel peminjaman
query_create_tabel_peminjaman = """
CREATE TABLE IF NOT EXISTS peminjaman(
  id_user INT,
  id_buku INT,
  user_name VARCHAR(40),
  nama_buku VARCHAR(40),
  tanggal_pinjam DATE,
  tanggal_kembali DATE,
  stock INT,
  FOREIGN KEY(id_user) REFERENCES user(id_user) ON DELETE SET NULL,
  FOREIGN KEY(id_buku) REFERENCES buku(id_buku) ON DELETE SET NULL
);
"""
mycursor.execute(query_create_tabel_peminjaman) # Mengeksekusi query
mydb.commit()


#main menu
exit = False

while not exit:
    main_menu = """
    ......LIBRARY MANAGEMENT......
    1. Pendaftaran User Baru
    2. Pendaftaran Buku Baru
    3. Peminjaman
    4. Tampilkan Daftar Buku
    5. Tampilkan Daftar User
    6. Tampilkan Daftar Peminjaman
    7. Cari Buku
    8. Pengembalian
    9. Exit
    """
    print(main_menu)
    
    selection = int(input("Masukan Nomer Tugas: "))
    
    if selection == 1:
        print ("Pendaftaran User Baru")
        mycursor.execute("INSERT INTO user (user_name, tgl_lahir, pekerjaan, alamat) VALUES (%s, %s, %s, %s)", 
                 (input("Masukan nama user: "),
                  input("Masukan tanggal lahir (YYYY-MM-DD):"),
                  input("Masukan Pekerjaan User: "),
                  input("Masukan Alamat User: ")))
        mydb.commit()
        print("Data User baru berhasil dimasukan")
    
    elif selection == 2:
        print ("Pendaftaran Buku Baru")
        # 2: Pendaftaran Buku Baru
        mycursor.execute("INSERT INTO buku (nama_buku, kategory_buku, stock) VALUES ( %s, %s, %s)", 
                 (input("Masukan Judul buku: "),
                  input("Masukan Kategory Buku: "),
                  input("Masukan Stock: ")))
        mydb.commit()
        print("Data buku berhasil dimasukan")
    
    elif selection == 3:
        print ("Peminjaman")
        id_user = int(input("masukan id: "))
        id_buku = int(input("masukan id buku: "))
        user_name = input("masukan nama: ")
        nama_buku = input("masukan nama buku: ")
        tanggal_pinjam = (today)
        tanggal_kembali = (today + timedelta(3))

        mycursor.execute("INSERT INTO peminjaman (id_user, id_buku, user_name, nama_buku, tanggal_pinjam, tanggal_kembali) VALUES ( %s, %s, %s, %s, %s, %s)",(id_user, id_buku, user_name , nama_buku, tanggal_pinjam, tanggal_kembali))
        mydb.commit()
        print("Query Berhasil dieksekusi")
        print("Buku Telah Dipinjamkan Kepada: " + str(user_name))
        mycursor.execute("UPDATE buku SET stock = stock - %s WHERE id_buku = %s;", (1, id_buku))
        mydb.commit()
    
    elif selection == 4:
        print ("Tampilkan Daftar Buku")
        mycursor.execute('SELECT * FROM buku;')
        daftar_buku = mycursor.fetchall()
        print ("ID Buku"+ "\t"+"Judul Buku" + "\t"+ "\t" + "Kategory Buku"+ "\t" + "\t" +"Stock")
        for detail_buku in daftar_buku:
            print (str(detail_buku[0]) + "\t" + detail_buku[1] + "\t"+ "\t"+ detail_buku[2]+ "\t"+ "\t" + str(detail_buku[3]))
    
    elif selection == 5:
        print ("Tampilkan Daftar User")
        #5. Menampilkan daftar user
        mycursor.execute('SELECT * FROM user;')
        daftar_user = mycursor.fetchall()
        print ("ID User"+ "\t" + "Nama User" + "\t"+ "Tanggal Lahir" + "\t" + "Pekerjaan")
        for detail_user in daftar_user:
            print (str(detail_user[0]) +"\t"+ detail_user[1] +"\t"+ "\t"+ detail_user[2] + "\t" + detail_user[3])
            
    elif selection == 6:
        print ("Tampilkan Daftar Peminjaman")
        #6. Menampilkan daftar Peminjaman)
        mycursor.execute('SELECT * FROM Peminjaman;')
        daftar_peminjaman = mycursor.fetchall()

        print ("ID User"+ "\t" + "ID Buku" + "\t"+ "Nama User" + "\t" + "Nama Buku" + "\t" + "Tanggal Pinjam" + "\t" + "Tanggal Pengembalian")
        for detail_peminjaman in daftar_peminjaman:
            print (str(detail_peminjaman[0]) +"\t" + 
                   str(detail_peminjaman[1]) +"\t" + 
                   str(detail_peminjaman[2]) + "\t" + "\t"+
                   detail_peminjaman[3] + "\t" + 
                   str(detail_peminjaman[4]) + "\t" + 
                   str(detail_peminjaman[5])
                  )
    elif selection == 7:
        print ("Cari Buku")
        #cari buku
        cari_buku = input("masukan nama buku: ")
        mycursor.execute("SELECT * FROM buku WHERE nama_buku = %s or nama_buku like %s;",(cari_buku,cari_buku))
        daftar_buku = mycursor.fetchall()
        mydb.commit()
        print ("ID Buku"+ "\t" + "\t" + "Judul Buku" + "\t" + "Kategory Buku"+ "\t" + "\t" +"Stock")
        for detail_buku in daftar_buku:
            print (str(detail_buku[0]) + "\t" + "\t" + detail_buku[1] + "\t"+ "\t"+ detail_buku[2]+ "\t"+ "\t" + str(detail_buku[3]))
    
    
    elif selection == 8:
        print ("Pengembalian")
        id_user = int(input("masukan id: "))
        id_buku = int(input("masukan id buku: "))
        print("Query Berhasil dieksekusi")
        print("Buku telah dikembalikan")

        #mycursor = mydb.cursor()  # membuat object cursor
        mycursor.execute('DELETE FROM peminjaman WHERE id_user= %s or id_buku = %s;', (id_user, id_buku))
        mydb.commit()
        mycursor.execute("UPDATE buku SET stock = stock + %s WHERE id_buku = %s;", (1, id_buku))
        mydb.commit()
    
    elif selection > 9:
        exit =  True
        print ("Input harus 1 sampai 9")
        print ("Program Selesai")
        print ("            ")
        print ("            ")
        mycursor.execute("DROP DATABASE tugas_LMS ")
        mydb.commit()
        mycursor.close()
        mydb.close()
        
    else:
        exit =  True
        print ("Program Selesai")
        print ("            ")
        mycursor.execute("DROP DATABASE tugas_LMS ")
        mydb.commit()
        mycursor.close()
        mydb.close()