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

USBSabertoothReplyReceiver::USBSabertoothReplyReceiver()
{
  reset();
}

void USBSabertoothReplyReceiver::read(byte data)
{
  if (data >= 128 || _ready) { reset(); }
  if (_length < SABERTOOTH_COMMAND_MAX_BUFFER_LENGTH) { _data[_length ++] = data; }
  
  if (_length >= 9 && _data[0] >= 128)
  {
    boolean crc = (_data[0] & 0x70) == 0x70; size_t length;
    
    switch (_data[1])
    {
    case SABERTOOTH_RC_GET:
      length = crc ? 10 : 9; break;
    
    default:
      return;
    }
    
    if (_length == length)
    {
      if (crc)
      {
        if (USBSabertoothCRC7::value(_data, 3) == _data[3])
        {
          uint16_t crc = USBSabertoothCRC14::value(_data + 4, length - 6);
          
          if (((crc >> 0) & 0x7f) == _data[length - 2] &&
              ((crc >> 7) & 0x7f) == _data[length - 1])
          {
            _data[0] &= ~0x70;
            _ready = true; _usingCRC = true;
          }
        }
      }
      else
      {
        if (USBSabertoothChecksum::value(_data, 3) == _data[3])
        {
          if (USBSabertoothChecksum::value(_data + 4, length - 5) == _data[length - 1])
          {
            _ready = true; _usingCRC = false;
          }
        }
      }
    }
  }
}

void USBSabertoothReplyReceiver::reset()
{
  _length = 0; _ready = false; _usingCRC = false;
}
