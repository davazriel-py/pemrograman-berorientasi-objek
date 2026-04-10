public class prak {
    
    public String nama;
    public String nim;
    public String kelas;
    public int angkatan;
    public String bahasa;
    public String negaraAsal;

    public prak(String nama, String nim, String kelas, int angkatan) {
        this.nama = nama;
        this.nim = nim;
        this.kelas = kelas;
        this.angkatan = angkatan;
        System.out.println("Data sudah disimpan kedalam database\n");
    }

    public void tampilkanInformasi() {
        System.out.println("INFORMASI MAHASISWA:");
        System.out.println("Nama: " + nama);
        System.out.println("NIM: " + nim);
        System.out.println("Kelas: " + kelas);
        System.out.println("Angkatan: " + angkatan);
    }

    public void setNama(String nama) {
        this.nama = nama;
    }

    private void setNim(String nim) {
        this.nim = nim;
    }

    protected void setKelas(String kelas) {
        this.kelas = kelas;
    }

    public String getNama() {
        return nama;
    }

}
