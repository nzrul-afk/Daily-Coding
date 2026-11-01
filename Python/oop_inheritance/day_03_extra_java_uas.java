public class day_03_extra_java_uas {
    public static void main(String[] args) {
        System.out.println("=== SIMULASI UAS JAVA: THE FINAL BOSS ===\n");
        
        babakSatuStringMemori();
        babakDuaMathCasting();
        babakTigaLoopSwitch();
        babakEmpatPassByValue();
        babakLimaBitwise();
    }

    // 1️⃣ String & Referensi Memori (== vs .equals)
    static void babakSatuStringMemori() {
        String a = "Polinema";
        String b = "Polinema";
        String c = new String("Polinema");

        System.out.println("Babak 1: String");
        System.out.println("Tebak 1 (a == b)     : " + (a == b));      // True
        System.out.println("Tebak 2 (a == c)     : " + (a == c));      // True
        System.out.println("Tebak 3 (a.equals(c)): " + (a.equals(c))); // True
        System.out.println("-------------------------------------------------");
    }

    // 2️⃣ Matematika: Integer Division & Narrowing Casting
    static void babakDuaMathCasting() {
        int x = 5;
        int y = 2;
        
        double hasil1 = x / y;
        double hasil2 = (double) x / y;
        byte angkaKecil = (byte) 130; // Batas byte adalah 127

        System.out.println("Babak 2: Math & Casting");
        System.out.println("Tebak 4 (hasil1): " + hasil1); // 2.0
        System.out.println("Tebak 5 (hasil2): " + hasil2); // 2.5
        System.out.println("Tebak 6 (130 di-cast ke byte): " + angkaKecil); // Berubah jadi minus berapa? 127
        System.out.println("-------------------------------------------------");
    }

    // 3️⃣ Increment (i++ vs ++i) & Switch Case Tanpa Break
    static void babakTigaLoopSwitch() {
        int i = 1;
        int total = 0;

        // Awas: i++ dipakai dulu nilainya (1) ke switch, lalu i berubah jadi 2.
        switch (i++) {
            case 1:
                total += i;     // i saat ini = 2. Total jadi 0 + 2 = 2.
            case 2:
                total += ++i;   // ++i jadi 3. Total jadi 2 + 3 = 5.
            case 3:
                total += i++;   // i++ masuk 3 dulu (Total 5 + 3 = 8), baru i jadi 4.
                break;
            default:
                total += 10;
        }

        System.out.println("Babak 3: Switch & Increment");
        System.out.println("Tebak 7 (total akhir): " + total); 
        System.out.println("Tebak 8 (i akhir): " + i);
        System.out.println("-------------------------------------------------");
    }

    // 4️⃣ Pass by Value (Variabel vs Array/Objek)
    static void babakEmpatPassByValue() {
        int angka = 10;
        int[] arrayAngka = {10};

        ubahData(angka, arrayAngka);

        System.out.println("Babak 4: Pass by Value");
        System.out.println("Tebak 9 (angka asli): " + angka);            // Tetap 10 atau berubah?
        System.out.println("Tebak 10 (arrayAngka[0]): " + arrayAngka[0]); // Tetap 10 atau berubah?
        System.out.println("-------------------------------------------------");
    }

    static void ubahData(int val, int[] arr) {
        val = 99;    
        arr[0] = 99; 
    }

    // 5️⃣ Operator Bitwise
    static void babakLimaBitwise() {
        int a = 5;
        int minus = -16;

        System.out.println("Babak 5: Bitwise");
        System.out.println("Tebak 11 (~5): " + (~a));           // Rumus: -(a + 1)
        System.out.println("Tebak 12 (-16 >> 2): " + (minus >> 2));   // Nilai minus dibagi 2^2
        System.out.println("Tebak 13 (-16 >>> 2): Positif Raksasa atau Minus? (Tebak jenisnya saja)"); 
    }
}