import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        Scanner input = new Scanner(System.in);

        System.out.print("Masukkan nama: ");
        String nama = input.nextLine();

        System.out.print("Masukkan NIM: ");
        String nim = input.nextLine();

        System.out.print("Masukkan kelas: ");
        String kelas = input.nextLine();

        System.out.print("Masukkan angkatan: ");
        int angkatan = input.nextInt();
        input.nextLine();

        System.out.print("Masukkan bahasa: ");
        String bahasa = input.nextLine();

        System.out.print("Masukkan negara asal: ");
        String negara = input.nextLine();

        System.out.print("Masukkan nilai: ");
        int nilai = input.nextInt();

        System.out.print("Apakah visa aktif? (true/false): ");
        boolean visa = input.nextBoolean();

        MahasiswaInternasional mhs = new MahasiswaInternasional(
                nama, nim, kelas, angkatan,
                bahasa, negara,
                nilai, visa
        );

        System.out.println("\n==============================");
        mhs.tampilkanInformasi("Dollar");

        input.close();
    }
}