#include <stdint.h>
#include <string.h>
static uint8_t ecc_f[256], ecc_b[256]; static uint32_t edc_t[256]; static int init=0;
static void ecc_init(void){
  for(uint32_t i=0;i<256;i++){ uint32_t j=(i<<1)^(i&0x80?0x11D:0); ecc_f[i]=j; ecc_b[i^j]=i;
    uint32_t e=i; for(int k=0;k<8;k++) e=(e>>1)^(e&1?0xD8018001:0); edc_t[i]=e; }
  init=1;
}
static void ecc_compute(const uint8_t*src,uint32_t maj_count,uint32_t min_count,uint32_t maj_mult,uint32_t min_inc,uint8_t*dest){
  uint32_t size=maj_count*min_count;
  for(uint32_t maj=0;maj<maj_count;maj++){
    uint32_t index=(maj>>1)*maj_mult+(maj&1); uint8_t a=0,b=0;
    for(uint32_t mn=0;mn<min_count;mn++){ uint8_t t=src[index]; index+=min_inc; if(index>=size) index-=size; a^=t; b^=t; a=ecc_f[a]; }
    a=ecc_b[ecc_f[a]^b]; dest[maj]=a; dest[maj+maj_count]=a^b;
  }
}
void fix_mode1(uint8_t*s){
  if(!init) ecc_init();
  uint32_t edc=0; for(int i=0;i<0x810;i++) edc=(edc>>8)^edc_t[(edc^s[i])&0xff];
  s[0x810]=edc; s[0x811]=edc>>8; s[0x812]=edc>>16; s[0x813]=edc>>24;
  memset(s+0x814,0,8);
  ecc_compute(s+0xC,86,24,2,86,s+0x81C);
  ecc_compute(s+0xC,52,43,86,88,s+0x8C8);
}
