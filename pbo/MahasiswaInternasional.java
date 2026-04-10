public class MahasiswaInternasional extends Mahasiswa {

    public String bahasa;
    public String negaraAsal;
    public int nilai;
    public boolean statusVisa;

    // Constructor
    public MahasiswaInternasional(String nama, String nim, String kelas, int angkatan,
                                  String bahasa, String negaraAsal,
                                  int nilai, boolean statusVisa) {

        super(nama, nim, kelas, angkatan);
        this.bahasa = bahasa;
        this.negaraAsal = negaraAsal;
        this.nilai = nilai;
        this.statusVisa = statusVisa;
    }

    public void tampilkanInformasi(String mataUang) {

        super.tampilkanInformasi();

        System.out.println("\nINFORMASI TAMBAHAN");
        System.out.println("Bahasa\t: " + bahasa);
        System.out.println("Negara\t: " + negaraAsal);
        System.out.println("Uang\t: " + mataUang);
        System.out.println("Nilai\t: " + nilai);

        // kondisi nilai
        if (nilai >= 75) {
            System.out.println("Mahasiswa LULUS");
        } 
        else if (nilai >= 60) {
            System.out.println("Remedial diperbolehkan");
        } 
        else {
            System.out.println("Harus mengulang, diperbolehkan memperpanjang masa tinggal (kepulangan ditunda)");
        }

        // kondisi visa
        if (statusVisa) {
            System.out.println("Visa aktif, mahasiswa diizinkan tinggal");
        } 
        else {
            System.out.println("Visa tidak aktif, segera lakukan perpanjangan");
        }

        // kondisi peringatan
        if (nilai < 60 && !statusVisa) {
            System.out.println("PERINGATAN: Mahasiswa harus mengulang dan segera memperpanjang visa!");
        }
    }
}