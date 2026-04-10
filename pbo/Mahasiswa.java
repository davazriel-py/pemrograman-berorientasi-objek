public class Mahasiswa {

    public String nama;
    public String nim;
    public String kelas;
    public int angkatan;

    public Mahasiswa(String nama, String nim, String kelas, int angkatan) {
        this.nama = nama;
        this.nim = nim;
        this.kelas = kelas;
        this.angkatan = angkatan;
    }

    public void tampilkanInformasi() {
        System.out.println("Nama : " + nama);
        System.out.println("NIM : " + nim);
        System.out.println("Kelas : " + kelas);
        System.out.println("Angkatan : " + angkatan);
    }
}