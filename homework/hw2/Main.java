package stevens.cs306.mac;

import java.security.Key;
import java.lang.*;

public class Main {

    public static void main(String[] args) {
        boolean verify = false;
        String message = "This is a test message.  There are many like it but"
            + " this one is mine.";
        String secret = "CS-306_Test_Key";
        byte[] tag = null;

        switch (args.length) {
            case 3:
                verify = true;
                tag = toByteArray(args[2]);
            case 2:
                secret = args[1];
            case 1:
                message = args[0];
                break;
            case 0:
                break;
            default:
                System.err.println("Unexpected number of params");
                usage();
                System.exit(1);
                break;
        }

        Mac mac = new Mac();
        Key key = mac.generate(secret.getBytes());

        System.err.println("## Key ##\n" + secret + "\n");
        System.err.println("## Message ##\n" + message + "\n");
        if (!verify) {
            tag = mac.mac(message.getBytes(), key);
        }
        System.err.println("## Tag ##\n" + toHexString(tag) + "\n");

        if (mac.verify(message.getBytes(), tag, key)) {
            System.err.println("Success, tag was verified.");
        } else {
            System.err.println("Error, tag was not verified.");
        }
    }

    public static String toHexString(byte[] array) {
        char[] hexArray = {'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};
        char[] hexChars = new char[array.length * 2];
        int v;
        for ( int j = 0; j < array.length; j++ ) {
            v = array[j] & 0xFF;
            hexChars[j*2] = hexArray[v/16];
            hexChars[j*2 + 1] = hexArray[v%16];
        }
        return new String(hexChars);
    }
      

    public static byte[] toByteArray(String s) {
        int len = s.length();
        byte[] data = new byte[len / 2];
        for (int i = 0; i < len; i += 2) {
            data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4)
                                 + Character.digit(s.charAt(i+1), 16));
        }
        return data;
    }
    

    public static void usage() {
        System.err.println("usage: java stevens.cs306.mac.Main [message [key [tag]]]");
    }

}
