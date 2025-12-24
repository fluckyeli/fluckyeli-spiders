# powGetP 是 VDF（可验证延迟函数）反爬虫机制


## 点击用户名输入框后，发送powGetP请求
```js
/*
负载：ed72279d0e51430a02d946f482f3f26ef55fe67674fce34b9c0f09f4b0c2e7cbfbb302f361b69dfae639d48f839abf7f3520d346ebea5c6d7fb9914d66d0c5993af0176b1c7f13691d1286f4e51310c00855ae5f8391b97ad7221703ac7f4030142ebc927691879be7055303019e6f4158a88a05412b3de3dd266eeb7ac4d33b
解密后：
{
  "pkid": "cjJVGQM",
  "pd": "imooc",
  "channel": 0,
  "topURL": "https://www.icourse163.org/",
  "rtid": "FdeRzc6dmgzHF17zjIooBZUKpajB31H5"
}

响应：
{
    "ret": "201",
    "pVInfo": {
        "needCheck": true,
        "sid": "d2540f9a-d6ea-47f8-9bec-ba614f339817",
        "hashFunc": "VDF_FUNCTION",
        "maxTime": 2050,
        "minTime": 2000,
        "args": {
            "mod": "5943f5607c99f4627bd7d3305a95d8056f",
            "t": 300000,
            "puzzle": "EuGk+BZrjtl1lvH0c0Ao9V2uX/T5NSvNe6HS5AMDJBvVUoibAy1wbhbVOmf7WbbgNGiy0SjS9wl5\r\nmai6PB2pGgp3rvK2o8bVJs6iNk7YhK3Fph8fRDuGTXMeDk5qKFc2bHDBzdA+BsVpxv+xlCKFJX6E\r\n1m8AIt2m1SgrQKc05jyeS+eFnSDT3+aCTUvsdd9xsaU+KyVLCgAmQOrFTLrogZginir8hi/SynYd\r\nzD64O1do9qyDaSsCkKvxH4e30Dty7GUrXVbM2HaDD1XewbD2SQ==",
            "x": "935cb0d4db"
        }
    }
}
 */

```

## 输入好用户名密码后，发起 /l 请求
```js
/*
负载：84497406fe47bded5c26fa9830987a1897e5c535ba12ddb8adc56c4deb988deb92610d36ae5e810ae3b593486b7a99c37ed5a618b086f14ecffc387b06ec224471d6f4f938ec9e04e3463c128831dac831d0848310aafda9e3cf6339309742db1163fd155b3b89abe5463c07da39006cec166326c803251be6590fbefbcaa24982b6df9e63cf471a016597c735cbd81535b166e8ca557a2d46e1fb0a44f9f3c63537b59a05842cb1bf00ccbe29851a02f016c14a31cf6694dc64f8ebfb16cc5cc16e108190c735265b87dc3d749337b19169d6d04dab8e6ad8331c4fcd4ce1fc82e40b9828e7a3de9c4f9c347f64e726b34923eaed737dc7bd6429cb1fb5e23001b7ee894ddf42da7c149de6c1837820640a29cbd2a62cf312bdf7a40f780303e2cef3ed14143f24e58b85335b7ff80757975398d93f413c5b9cced542fd1fd5a68462f8ae1e67ec3003bc65d98af809f2264615e099a8a70ca7cbccd78c80e298eff5ad302b3773a975be2f720c702f3831ce4a774f3faee0f8cfa1956cfa979310b1f8ff66a7cf3f7c0938c7184af2fc3ee08fcd85730e1a9f84c2106d87f4369c2cd10138d04cee6b456b80ba5853b4a4341ef2a6b49290f894cf8d82bf138f23a0f66b1a978c7ed783af62ad95f9cbd01f8e93211abeebffb67b0d5bcd82c98a420b623aed1469967dade84e57eb968c940d750316d464d260c9b0abff17b77f8529d8987cbafbcb18ed4ffd3a1486e3478393ac476cedd9630bb2e940bdce917cc45441c5a410e687215eb34265062f1c8c41ac02650afafa86a5a4696fe1807af23f861d8a59422544314dc7e7afe0b358dc7ba577c3a984c41a732a03a8882da0e89eb28209dda0b1feb4dbbf4998364332a03d2d0a313f0adb1aa5e327b424b9e2b49d6b9c21166f257135bc464390256e5b780b9061488c43332be44f2ed2083c6ccb0f4c08d46b152248e3e826b0da86654fd914a3b3ad824ae2c09c990e49ab9ef7dd87be82c5bc249998ff5404728de845f604e45431e6afd356761240d87ff5af3a1057cc92f7ab9cea5ed3dee50dda61c8de21d9fb19543d9b66047b817010fa1ad9c6eb8fbe5fa6a5daf9bc1f847bbbbcd9c58d854d2a891ade06efcf89f52e8837ab7a798a55c5680895db2009da9167d379bf08e1ed9dee8d7b7d257b196e9c3acbacff0df33be789176f4f3164b73bdaef4c413f88c9f5ccb6e79eba4ef4685f53913b0a70d3d1fbb513a44e2408e5347679d5fa528c2cc4dadbec96604bfb92db52a90446eb2d
解密后：
{
  "un": "test123@163.com",
  "pw": "LO/+/Nt99kwDB/+=",
  "pd": "imooc",
  "l": 1,
  "d": 10,
  "t": 1766061612994,
  "pkid": "cjJVGQM",
  "domains": "",
  "tk": "93368f546a6b0a656eaa355aa0f79586",
  "pwdKeyUp": 1,
  "pVParam": {
    "puzzle": "EuGk+BZrjtl1lvH0c0Ao9V2uX/T5NSvNe6HS5AMDJBvVUoibAy1wbhbVOmf7WbbgNGiy0SjS9wl5\r\nmai6PB2pGgp3rvK2o8bVJs6iNk7YhK3Fph8fRDuGTXMeDk5qKFc2bHDBzdA+BsVpxv+xlCKFJX6E\r\n1m8AIt2m1SgrQKc05jyeS+eFnSDT3+aCTUvsdd9xsaU+KyVLCgAmQOrFTLrogZginir8hi/SynYd\r\nzD64O1do9qyDaSsCkKvxH4e30Dty7GUrXVbM2HaDD1XewbD2SQ==",
    "spendTime": 2000,
    "runTimes": 719399,
    "sid": "d2540f9a-d6ea-47f8-9bec-ba614f339817",
    "args": "{\"x\":\"538d20bf889d27f5b89fcdf00ad74086bc\",\"t\":719399,\"sign\":3660720468}"
  },
  "channel": 0,
  "topURL": "https://www.icourse163.org/",
  "rtid": "sSWHqxY0U1mEyiFE3L87oBEBw9kF76IH"
}

 */
```