# SAMI Data Reduction



## Example Data

- 150422
  - ccd_1 
    - 22apr10001.fits 
    - 22apr10003.fits 
    - 22apr10036.fits 
    - 22apr10074.fits 
    - 22apr10078.fits
    - 22apr10002.fits 
    - 22apr10035.fits 
    - 22apr10037.fits 
    - 22apr10075.fits 
    - 22apr10079.fits
  - ccd_2
    - 22apr20074.fits 
    - 22apr20075.fits 
    - 22apr20078.fits 
    - 22apr20079.fits



### `.idx` file:

**Blue Arm**: `sami580V.idx`

**Red arm**: `sami1000R.idx`

## Identification of Calibrations

Required calibration files are:

- a fibre flat field, with `ndf_class` of `MFFFF`
- an arc, with `ndf_class` of `MFARC`



Object files have `ndf_class` of `MFOBJECT`



## Steps Required

1. Produce a Tram Line Map
2. Measure the wavelength calibration
3. Measure a flatfield
4. Reduce Objects



## Typical Reduction commands

```bash
aaorun reduce_fflat 22apr20074.fits -idxfile sami1000R.idx -OUT_DIRNAME 22apr20026_outdir -USEFLATIM 0
aaorun reduce_arc 22apr20075.fits -idxfile sami1000R.idx -OUT_DIRNAME 22apr20075_outdir -EXTR_OPERATION GAUSS -USEFLATIM 0 -TLMAP_FILENAME 22apr20074tlm.fits
aaorun reduce_fflat 22apr20074.fits -idxfile sami1000R.idx -OUT_DIRNAME 22apr20074_outdir -WAVEL_FILENAME 22apr20075red.fits
aaorun reduce_object 14apr20023.fits -idxfile sami1000R.idx -OUT_DIRNAME 14apr20023_outdir -TLMAP_FILENAME 14apr20026tlm.fits -WAVEL_FILENAME 14apr20025red.fits -FFLAT_FILENAME 14apr20026red.fits
```