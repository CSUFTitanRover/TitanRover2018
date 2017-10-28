/*
Arduino Library for USB Sabertooth Packet Serial
Copyright (c) 2012-2013 Dimension Engineering LLC
http://www.dimensionengineering.com/arduino

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER
RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE
USE OR PERFORMANCE OF THIS SOFTWARE.
*/

#include "USBSabertooth.h"

void USBSabertoothCRC14::begin()
{
  _crc = 0x3fff;
}

void USBSabertoothCRC14::write(byte data)
{
  _crc ^= data;
  
  for (byte bit = 0; bit < 8; bit ++)
  {
    if (_crc & 1)
    {
      _crc >>= 1; _crc ^= 0x22f0;
    }
    else
    {
      _crc >>= 1;
    }
  }
}

void USBSabertoothCRC14::write(const byte* data, size_t lengthOfData)
{
  for (size_t i = 0; i < lengthOfData; i ++) { write(data[i]); }
}

void USBSabertoothCRC14::end()
{
  _crc ^= 0x3fff;
}

uint16_t USBSabertoothCRC14::value(const byte* data, size_t lengthOfData)
{
  USBSabertoothCRC14 crc;
  crc.begin(); crc.write(data, lengthOfData); crc.end();
  return crc.value();
}
