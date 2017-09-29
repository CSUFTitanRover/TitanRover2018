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

USBSabertooth::USBSabertooth(USBSabertoothSerial& serial, byte address)
  : _address(address), _serial(serial)
{
  init();
}

void USBSabertooth::init()
{
  useCRC();
  setGetRetryInterval(SABERTOOTH_DEFAULT_GET_RETRY_INTERVAL);
  setGetTimeout(SABERTOOTH_DEFAULT_GET_TIMEOUT);
}

void USBSabertooth::command(byte command,
                            byte value)
{
  this->command(command, &value, 1);
}

void USBSabertooth::command(byte command,
                            const byte* value, size_t bytes)
{
  USBSabertoothCommandWriter::writeToStream(_serial.port(), address(),
                                            (USBSabertoothCommand)command,
                                            usingCRC(), value, bytes);
}

void USBSabertooth::motor(int value)
{
  motor(1, value);
}

void USBSabertooth::motor(byte number, int value)
{
  set('M', number, value);
}

void USBSabertooth::power(int value)
{
  power(1, value);
}

void USBSabertooth::power(byte number, int value)
{
  set('P', number, value);
}

void USBSabertooth::drive(int value)
{
  motor('D', value);
}

void USBSabertooth::turn(int value)
{
  motor('T', value);
}

void USBSabertooth::freewheel(int value)
{
  freewheel(1, value);
}

void USBSabertooth::freewheel(byte number, int value)
{
  set('Q', number, value);
}

void USBSabertooth::shutDown(byte type, byte number, boolean value)
{
  set(type, number, value ? 2048 : 0, SABERTOOTH_SET_SHUTDOWN);
}

void USBSabertooth::setRamping(int value)
{
  setRamping('*', value);
}

void USBSabertooth::setRamping(byte number, int value)
{
  set('R', number, value);
}

void USBSabertooth::setTimeout(int milliseconds)
{
  set('M', '*', milliseconds, SABERTOOTH_SET_TIMEOUT);
}

void USBSabertooth::keepAlive()
{
  set('M', '*', 0, SABERTOOTH_SET_KEEPALIVE);
}

int USBSabertooth::get(byte type, byte number,
                       USBSabertoothGetType getType, boolean unscaled)
{
  USBSabertoothTimeout timeout(getGetTimeout());
  USBSabertoothTimeout retry(getGetRetryInterval()); retry.expire();
  
  byte flags = (byte)getType;
  if (unscaled) { flags |= 2; }
  
  USBSabertoothReplyReceiver receiver;
  USBSabertoothReplyCode replyCode = SABERTOOTH_RC_GET;
  
  while (1)
  {
    if (timeout.expired())
    {
      return SABERTOOTH_GET_TIMED_OUT;
    }
    
    if (retry.expired())
    {
      retry.reset();
      
      byte data[3];
      data[0] = flags;
      data[1] = type;
      data[2] = number;
      
      command(SABERTOOTH_CMD_GET,
              data, sizeof(data));
    }
    
    if (!_serial.tryReceivePacket ()              ) { continue; }
    if (_serial._receiver.address () != address() ) { continue; }
    if (_serial._receiver.command () != replyCode ) { continue; }
    if (_serial._receiver.usingCRC() != usingCRC()) { continue; }
    
    const byte* data = _serial._receiver.data();
    if (flags  == (data[2] & ~1) &&
        type   ==  data[6]       &&
        number ==  data[7])
    {
      int16_t value = (uint16_t)data[4] << 0 |
                      (uint16_t)data[5] << 7 ;
      return (data[2] & 1) ? -value : value;
    }
  }
}

void USBSabertooth::set(byte type, byte number, int value)
{
  set(type, number, value, SABERTOOTH_SET_VALUE);
}

void USBSabertooth::set(byte type, byte number, int value,
                         USBSabertoothSetType setType)
{
  byte flags = (byte)setType;
  if (value < -SABERTOOTH_MAX_VALUE) { value = -SABERTOOTH_MAX_VALUE; }
  if (value >  SABERTOOTH_MAX_VALUE) { value =  SABERTOOTH_MAX_VALUE; }
  if (value <                     0) { value = -value;   flags |=  1; }
  
  byte data[5];
  data[0] = flags;
  data[1] = (byte)((uint16_t)value >> 0) & 0x7f;
  data[2] = (byte)((uint16_t)value >> 7) & 0x7f;
  data[3] = type;
  data[4] = number;
  
  command(SABERTOOTH_CMD_SET, data, sizeof(data));
}
