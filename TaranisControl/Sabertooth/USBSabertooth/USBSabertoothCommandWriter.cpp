/*
Arduino Library for USB Sabertooth Packet Serial
Copyright (c) 2013 Dimension Engineering LLC
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

size_t USBSabertoothCommandWriter::writeToBuffer(byte* buffer, byte address,
                                                 USBSabertoothCommand command, boolean useCRC,
                                                 const byte* data, size_t lengthOfData)
{
  size_t i = 0;
  
  if (useCRC) { address |= 0xf0; }
  buffer[i ++] = address;
  buffer[i ++] = (byte)command;
  buffer[i ++] = data[0];
  buffer[i ++] = useCRC
    ? USBSabertoothCRC7::value(buffer, 3)
    : USBSabertoothChecksum::value(buffer, 3);
  
  if (lengthOfData > 1)
  {
    for (size_t j = 1; j < lengthOfData; j ++) { buffer[i ++] = data[j]; }
    
    if (useCRC)
    {
      uint16_t crc = USBSabertoothCRC14::value(buffer + 4, lengthOfData - 1);
      buffer[i ++] = (crc >> 0) & 0x7f;
      buffer[i ++] = (crc >> 7) & 0x7f;
    }
    else
    {
      buffer[i ++] = USBSabertoothChecksum::value(buffer + 4, lengthOfData - 1);
    }
  }
  
  return i;
}

void USBSabertoothCommandWriter::writeToStream(Stream& port, byte address,
                                               USBSabertoothCommand command, boolean useCRC,
                                               const byte* data, size_t lengthOfData)
{
  byte buffer[SABERTOOTH_COMMAND_MAX_BUFFER_LENGTH];
  size_t lengthOfBuffer = writeToBuffer(buffer, address, command, useCRC, data, lengthOfData);
  port.write(buffer, lengthOfBuffer);
}
