# QrCode

## Ziele

- [x] Grobe Datenanalyse/Datenverwaltung: Passende Kodierung wählen (numerisch, alphanumerisch, Byte (Latin-1) und Kanji (shift JIS))
- [x] Minimale Version (bzw. Größe) berechnen, padding und in Codewörter unterteilen
- [x] Error Correction Coding: Redundante Bytes zur Fehlerbehebung berechnen (Reed-Solomon-Code)
- [x] Zahlen im Galois-Feld GF(256)
- [x] Generator-Polynom und Message-Polynom erstellen
- [x] Polynomen Division
- [x] Die Daten passend sortieren, sodass der QR-Code gefüllt werden kann
- [x] Den QR-Code mit function patterns füllern
- [x] Die QR-Code Matrix mit den Daten und dessen Fehlerkorrektur füllen
- [ ] Maskieren des QR-Codes
- [ ] Versions Informationen+Fehlerkorrekturbits erstellen
- [ ] Versions Informationen in den QR-Code einfügen
- [ ] Format Informationen+Fehlerkorrekturbits erstellen
- [ ] Format Informationen in den QR-Code einfügen

## Resources

- [Thonky's QR Code tutorial](https://www.thonky.com/qr-code-tutorial/)

## Resources, not used

- [QR Code Data Capacity](https://blog.qr4.nl/page/QR-Code-Data-Capacity.aspx)
- [Information capacity and versions of the QR Code](https://www.qrcode.com/en/about/version.html)
- [QR Code Library for Lua](https://speedata.github.io/luaqrcode/docs/qrencode.html)
- [Galois Finite Fields and the Advanced Encryption Standard (AES)](https://www.cs.uaf.edu/2015/spring/cs463/lecture/03_23_AES.html)
- [AES Proposal: Rijndael](https://csrc.nist.gov/csrc/media/projects/cryptographic-standards-and-guidelines/documents/aes-development/rijndael-ammended.pdf)
- [An Intro to Finite Fields](https://www.cantorsparadise.com/the-theory-and-applications-of-finite-fields-e78844896eaa)
