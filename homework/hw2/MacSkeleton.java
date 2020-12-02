package stevens.cs306.mac;

import java.security.Key;
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.spec.SecretKeySpec;

// DO NOT MODIFY
public abstract class MacSkeleton {

    public static final String KEY_ALGO = "AES";
    public static final String MODE = KEY_ALGO + "/ECB/NoPadding";
    public static final int BLOCK_SIZE = 128 / 8;
    public static final int KEY_SIZE = 128 / 8;

    public static int getBlockSize() {
        return BLOCK_SIZE;
    }

    /**
     * Generates a key given some secret.  Pads or truncates it to the correct
     * key size.
     * @param secret    Secret to generate key from
     * @return          A Key generated from the secret
     */
    public static Key generate(byte[] secret) {
        byte[] key = new byte[KEY_SIZE];
        System.arraycopy(secret, 0, key, 0, Math.min(secret.length, KEY_SIZE));
        return new SecretKeySpec(key, KEY_ALGO);
    }

    /**
     * Performs a bitwise XOR on two byte arrays and returns the result as
     * a new byte array.
     * @param a     First byte array
     * @param b     Second byte array
     * @return      The result of a bitwise XOR of both arrays.
     */
    public static byte[] xor(byte[] a, byte[] b) {
        byte[] rv = new byte[Math.max(a.length, b.length)];
        System.arraycopy((a.length > b.length ? a : b), 0, rv, 0, rv.length);
        for (int i = 0, l = Math.min(a.length, b.length); i < l; ++i) {
            rv[i] = (byte) (a[i] ^ b[i]);
        }
        return rv;
    }

    /**
     * Takes a message and a block size in bytes and pads the message to that
     * block size with 100...  Adds an additional block if needed.
     * @param message   message to pad
     * @param blockSz   block size to pad the message to
     * @return          message padded out to the right block size
     */
    public static byte[] pad(byte[] message, int blockSz) {
        byte[] rv = new byte[((message.length/blockSz) + 1) * blockSz];
        System.arraycopy(message, 0, rv, 0, message.length);
        rv[(message.length)] = (byte) 0x80;
        return rv;
    }

    /**
     * Encrypts a single block.  Input block must be of the correct block
     * size.
     * @param block     A single block of plaintext, of size BLOCK_SIZE
     * @param key       The key to use for encrypting the plaintext 
     * @return          The ciphertext generated from encrypting the plaintext
     */
    public static byte[] encryptBlock(byte[] block, Key key) throws Exception {
        if (block == null || block.length != BLOCK_SIZE) {
            throw new IllegalArgumentException(
                "Block must be size " + BLOCK_SIZE);
        }

        Cipher c = Cipher.getInstance(MODE);
        c.init(Cipher.ENCRYPT_MODE, key);
        return c.doFinal(block);
    }

    public abstract byte[] mac(byte[] message, Key key);
    public abstract boolean verify(byte[] message, byte[] tag, Key key);

}

