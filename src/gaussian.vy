# @version ^0.4.0

# vygauss: Vyper library for statistical functions with error < 1e-8
# Ported from solgauss (Solidity)

ONE: constant(uint256) = 10 ** 18
ONE_SIGNED: constant(int256) = 10 ** 18
ONE_SQUARED: constant(int256) = 10 ** 36
TWO: constant(uint256) = 2 * 10 ** 18
POW: constant(uint256) = 96
SQRT2_WAD: constant(int256) = 1414213562373095048

POW96_VAL: constant(int256) = 79228162514264337593543950336

# ERFC coefficients - numerator
ERFC_NUM_0: constant(int256) = 2390663486789119588702562760758
ERFC_NUM_1: constant(int256) = 30799163124163494728815611822912
ERFC_NUM_2: constant(int256) = 217009993805181888096653824035967
ERFC_NUM_3: constant(int256) = 872769759520831409727955510614625
ERFC_NUM_4: constant(int256) = 1770156059949187207368715502030199
ERFC_NUM_5: constant(int256) = 491827887548901059160308996468717
ERFC_NUM_6: constant(int256) = 2951903062606160425784903342898012
ERFC_NUM_7: constant(int256) = 10696943466755803971902744822517940
ERFC_NUM_8: constant(int256) = 66754282175154591985610265743670774
ERFC_NUM_9: constant(int256) = 118123357223642876698647512612484570
ERFC_NUM_10: constant(int256) = 74612267035072815575090161964147929

# ERFC coefficients - denominator
ERFC_DEN_0: constant(int256) = 233007495570756707611067185269
ERFC_DEN_1: constant(int256) = 1000982532171916462620503333604
ERFC_DEN_2: constant(int256) = 1193288078754614002642444061841
ERFC_DEN_3: constant(int256) = 2623865187999034433680727904743

# ERFC upper bound (4.0523 scaled by 2^96)
ERFC_UPPER: constant(int256) = 321056282956553358679555000716

# ERFC scale factor (signed negative)
ERFC_SCALE: constant(int256) = -35166673128386

# ERFINV boundaries (input scaled by 2^96)
# 0.99 WAD scaled by 2^96 is 0xf5c28f5c28f5c28f5c28f5c2
ERFINV_0_99: constant(int256) = 76059036013693764089802192322
# 0.9999 WAD scaled by 2^96 is 0xfd70a3d70a3d70a3d70a3d70  
ERFINV_0_9999: constant(int256) = 78435880889121694217608510832

# ERFINV 0-0.99 coefficients - numerator (from hex values)
ERFINV1_NUM_0: constant(int256) = 331353699369447034452059835477
ERFINV1_NUM_1: constant(int256) = 258233142497643179939648346147
ERFINV1_NUM_2: constant(int256) = 2488781860465959717234601326710
ERFINV1_NUM_3: constant(int256) = 2738590283898461018322627916641
ERFINV1_NUM_4: constant(int256) = 944583020602364863721848760500
ERFINV1_NUM_5: constant(int256) = 2878671694187401374675030938962
ERFINV1_NUM_6: constant(int256) = 1173946478208979691168897580971
ERFINV1_NUM_7: constant(int256) = 78571753881288783598

# ERFINV 0-0.99 coefficients - denominator
ERFINV1_DEN_0: constant(int256) = 315108062651758531662122605793
ERFINV1_DEN_1: constant(int256) = 87703403749895136110982270537
ERFINV1_DEN_2: constant(int256) = 1044658544818372072826136154071
ERFINV1_DEN_3: constant(int256) = 1291137726893549314369655859999
ERFINV1_DEN_4: constant(int256) = 235581255707931908410929886899
ERFINV1_DEN_5: constant(int256) = 1064239241597319929447490324331
ERFINV1_DEN_6: constant(int256) = 434005836621884562572279122113

ERFINV1_SCALE: constant(int256) = 327636457319539409

# ERFINV 0.99-0.9999 coefficients - numerator
ERFINV2_NUM_0: constant(int256) = 33673697534270478588220456830
ERFINV2_NUM_1: constant(int256) = 397848153802874170266269747741
ERFINV2_NUM_2: constant(int256) = 580109727101714805548766417663
ERFINV2_NUM_3: constant(int256) = 227816579248216510236099340590

# ERFINV 0.99-0.9999 coefficients - denominator
ERFINV2_DEN_0: constant(int256) = 358111721368516139011808808945
ERFINV2_DEN_1: constant(int256) = 601292241278275875325241663854
ERFINV2_DEN_2: constant(int256) = 445186027765516940870479236216
ERFINV2_DEN_3: constant(int256) = 122777379491721666491792761570

ERFINV2_SCALE: constant(int256) = -160778573757846368

# ERFINV high-range (0.9999-1) coefficients (from Solidity hex values)
ERFINV3_NUM_0: constant(int256) = 774545014278341407       # 0xabfbc96369c431f
ERFINV3_NUM_1: constant(int256) = 22723844989269184583     # 0x13b5b509f246e1047
ERFINV3_NUM_2: constant(int256) = 241780725177450611770    # 0xd1b61b08a2a49c43a
ERFINV3_NUM_3: constant(int256) = 1270458252452368382580   # 0x44df26696ddaf67a74
ERFINV3_NUM_4: constant(int256) = 3647848324763204605040   # 0xc5c010a43e4e965470
ERFINV3_NUM_5: constant(int256) = 5769497221460691405500   # 0x138c3dbb2cfe7ba4abc
ERFINV3_NUM_6: constant(int256) = 4630337846156545295900   # 0xfb02d89a7f8035061c
ERFINV3_NUM_7: constant(int256) = 1423437110749683577340   # 0x4d2a287e88a740f1fc

ERFINV3_DEN_0: constant(int256) = 1485985001               # 0x589254e9
ERFINV3_DEN_1: constant(int256) = 774414590651577          # 0x2c0537295acb9
ERFINV3_DEN_2: constant(int256) = 21494160384252876        # 0x4c5cd33272dbcc
ERFINV3_DEN_3: constant(int256) = 209450652105127491       # 0x2e81e4224b33643
ERFINV3_DEN_4: constant(int256) = 975478320017874271       # 0xd89985d1ec29d5f
ERFINV3_DEN_5: constant(int256) = 2370766162602453236      # 0x20e6a743976f68f4
ERFINV3_DEN_6: constant(int256) = 2903651444541994617      # 0x284bd79ac779b679
ERFINV3_DEN_7: constant(int256) = 1414213562373095048      # 0x13a04bbdfdc9be88 (sqrt(2) * WAD)

ERFINV3_SCALE: constant(int256) = 1000000000000000         # 0x38d7ea4c68000 (1e15)

INV_SQRT2_96: constant(int256) = 56022770974786139918731938227

LN2_WAD: constant(int256) = 693147180559945309

# Constants for Solady's lnWad polynomial approximation
# Lookup table for fine log2 bits (packed as bytes32)
LN_LOOKUP: constant(uint256) = 112615256668934141757608348301524576118889381898850656584596385199644032892927
LN_MAGIC: constant(uint256) = 175629608733387594055579892975202555070

# lnWad polynomial coefficients
LN_P0: constant(int256) = 3273285459638523848632254066296
LN_P1: constant(int256) = 24828157081833163892658089445524
LN_P2: constant(int256) = 43456485725739037958740375743393
LN_P3: constant(int256) = 11111509109440967052023855526967
LN_P4: constant(int256) = 45023709667254063763336534515857
LN_P5: constant(int256) = 14706773417378608786704636184526
LN_P6: constant(int256) = 795164235651350426258249787498

LN_Q0: constant(int256) = 5573035233440673466300451813936
LN_Q1: constant(int256) = 71694874799317883764090561454958
LN_Q2: constant(int256) = 283447036172924575727196451306956
LN_Q3: constant(int256) = 401686690394027663651624208769553
LN_Q4: constant(int256) = 204048457590392012362485061816622
LN_Q5: constant(int256) = 31853899698501571402653359427138
LN_Q6: constant(int256) = 909429971244387300277376558375

# Scale factors for lnWad
LN_SCALE: constant(int256) = 1677202110996718588342820967067443963516166
LN_LN2_SCALE: constant(int256) = 16597577552685614221487285958193947469193820559219878177908093499208371
LN_OFFSET: constant(int256) = 600920179829731861736702779321621459595472258049074101567377883020018308


@internal
@pure
def _sqrt(x: uint256) -> uint256:
    if x == 0:
        return 0
    
    z: uint256 = 181
    
    r: uint256 = 0
    if x > 340282366920938463463374607431768211455:
        r = 128
    if (x >> r) > 18446744073709551615:
        r = r + 64
    if (x >> r) > 4294967295:
        r = r + 32
    if (x >> r) > 65535:
        r = r + 16
    
    z = z << (r >> 1)
    z = (z * ((x >> r) + 65536)) >> 18
    
    z = (z + x // z) >> 1
    z = (z + x // z) >> 1
    z = (z + x // z) >> 1
    z = (z + x // z) >> 1
    z = (z + x // z) >> 1
    z = (z + x // z) >> 1
    z = (z + x // z) >> 1
    
    if x // z < z:
        z = z - 1
    
    return z


@internal
@pure
def _ln_wad(x: int256) -> int256:
    """
    @notice Compute ln(x) where x is WAD-scaled (1e18), returns WAD-scaled result
    @dev Port of Solady's lnWad using (8,8) rational polynomial approximation
    """
    assert x > 0, "ln undefined"
    
    _x: uint256 = convert(x, uint256)
    
    # Compute r = 255 - floor(log2(x)) using bit comparisons
    # r starts as bits indicating magnitude
    r: uint256 = 0
    if _x > 340282366920938463463374607431768211455:  # > 2^128 - 1
        r = 128
    if (_x >> r) > 18446744073709551615:  # > 2^64 - 1
        r = r | 64
    if (_x >> r) > 4294967295:  # > 2^32 - 1
        r = r | 32
    if (_x >> r) > 65535:  # > 2^16 - 1
        r = r | 16
    if (_x >> r) > 255:  # > 2^8 - 1
        r = r | 8
    
    # Fine-tune r using lookup table for the remaining bits
    # In Solidity: shr(shr(r, x), magic) means magic >> (x >> r)
    shifted: uint256 = _x >> r
    lookup_index: uint256 = (LN_MAGIC >> shifted) & 31
    # Extract byte from lookup table: byte at position lookup_index
    lookup_byte: uint256 = (LN_LOOKUP >> (248 - 8 * lookup_index)) & 255
    r = r ^ lookup_byte
    
    # Reduce x to range [1, 2) * 2^96
    # x = x * 2^(159 - r) >> 159 = x << r >> 159
    x_reduced: int256 = convert((_x << r) >> 159, int256)
    
    p: int256 = LN_P0 + x_reduced
    p = ((p * x_reduced) >> 96) + LN_P1
    p = ((p * x_reduced) >> 96) + LN_P2
    p = ((p * x_reduced) >> 96) - LN_P3
    p = ((p * x_reduced) >> 96) - LN_P4
    p = ((p * x_reduced) >> 96) - LN_P5
    p = (p * x_reduced) - (LN_P6 << 96)  # Leave in 2^192 basis
    
    # q polynomial
    q: int256 = x_reduced + LN_Q0
    q = ((x_reduced * q) >> 96) + LN_Q1
    q = ((x_reduced * q) >> 96) + LN_Q2
    q = ((x_reduced * q) >> 96) + LN_Q3
    q = ((x_reduced * q) >> 96) + LN_Q4
    q = ((x_reduced * q) >> 96) + LN_Q5
    q = ((x_reduced * q) >> 96) + LN_Q6
    
    # p / q (no scaling needed, p is already 2^96 too large)
    p = p // q
    
    # Apply scale factor: s * 5^18 * 2^96
    p = LN_SCALE * p
    
    # Add ln(2) * k * 5^18 * 2^192 where k = 159 - r
    # Note: r can be > 159, so we compute as signed to avoid underflow
    p = p + LN_LN2_SCALE * (159 - convert(r, int256))
    
    # Add ln(2^96 / 10^18) * 5^18 * 2^192
    p = p + LN_OFFSET
    
    # Base conversion: divide by 2^174 (shift right 174)
    result: int256 = p >> 174
    
    return result


@internal
@pure
def _erfc_internal(x: int256) -> uint256:
    mask: int256 = x >> 255
    z: int256 = (x ^ mask) - mask
    
    y: uint256 = 0
    
    if z < ERFC_UPPER:
        num: int256 = z - ERFC_NUM_0
        num = ((num * z) >> POW) + ERFC_NUM_1
        num = ((num * z) >> POW) - ERFC_NUM_2
        num = ((num * z) >> POW) + ERFC_NUM_3
        num = ((num * z) >> POW) - ERFC_NUM_4
        num = ((num * z) >> POW) + ERFC_NUM_5
        num = ((num * z) >> POW) + ERFC_NUM_6
        num = ((num * z) >> POW) + ERFC_NUM_7
        num = ((num * z) >> POW) - ERFC_NUM_8
        num = ((num * z) >> POW) + ERFC_NUM_9
        num = ((num * z) >> POW) - ERFC_NUM_10
        
        denom: int256 = z - ERFC_DEN_0
        denom = ((denom * z) >> POW) + ERFC_DEN_1
        denom = ((denom * z) >> POW) - ERFC_DEN_2
        denom = ((denom * z) >> POW) + ERFC_DEN_3
        
        y = convert((ERFC_SCALE * num) // denom, uint256)
    
    if x < 0:
        y = TWO - y
    
    return y


@internal
@pure
def _erfinv_internal(x: int256) -> int256:
    mask: int256 = x >> 255
    z: int256 = (x ^ mask) - mask
    
    y: int256 = 0
    
    if z < ERFINV_0_99:
        num: int256 = z - ERFINV1_NUM_0
        num = ((num * z) >> POW) - ERFINV1_NUM_1
        num = ((num * z) >> POW) + ERFINV1_NUM_2
        num = ((num * z) >> POW) - ERFINV1_NUM_3
        num = ((num * z) >> POW) - ERFINV1_NUM_4
        num = ((num * z) >> POW) + ERFINV1_NUM_5
        num = ((num * z) >> POW) - ERFINV1_NUM_6
        num = ((num * z) >> POW) + ERFINV1_NUM_7
        
        denom: int256 = z - ERFINV1_DEN_0
        denom = ((denom * z) >> POW) + ERFINV1_DEN_1
        denom = ((denom * z) >> POW) + ERFINV1_DEN_2
        denom = ((denom * z) >> POW) - ERFINV1_DEN_3
        denom = ((denom * z) >> POW) - ERFINV1_DEN_4
        denom = ((denom * z) >> POW) + ERFINV1_DEN_5
        denom = ((denom * z) >> POW) - ERFINV1_DEN_6
        
        y = (ERFINV1_SCALE * num) // denom
        
    elif z < ERFINV_0_9999:
        num: int256 = z - ERFINV2_NUM_0
        num = ((num * z) >> POW) - ERFINV2_NUM_1
        num = ((num * z) >> POW) + ERFINV2_NUM_2
        num = ((num * z) >> POW) - ERFINV2_NUM_3
        
        denom: int256 = z - ERFINV2_DEN_0
        denom = ((denom * z) >> POW) + ERFINV2_DEN_1
        denom = ((denom * z) >> POW) - ERFINV2_DEN_2
        denom = ((denom * z) >> POW) + ERFINV2_DEN_3
        
        y = (ERFINV2_SCALE * num) // denom
        
    else:
        z_scaled: int256 = (z * ONE_SIGNED) // POW96_VAL
        
        one_minus_z: uint256 = convert(ONE_SIGNED - z_scaled, uint256)
        if one_minus_z == 0:
            one_minus_z = 1
        
        ln_val: int256 = self._ln_wad(convert(one_minus_z, int256))
        under_sqrt: int256 = LN2_WAD - ln_val
        if under_sqrt < 0:
            under_sqrt = 0
        
        r: int256 = convert(self._sqrt(convert(under_sqrt, uint256) * ONE), int256)
        r = r - 1600000000000000000
        
        num: int256 = (ERFINV3_NUM_0 * r) // ONE_SIGNED + ERFINV3_NUM_1
        num = (num * r) // ONE_SIGNED + ERFINV3_NUM_2
        num = (num * r) // ONE_SIGNED + ERFINV3_NUM_3
        num = (num * r) // ONE_SIGNED + ERFINV3_NUM_4
        num = (num * r) // ONE_SIGNED + ERFINV3_NUM_5
        num = (num * r) // ONE_SIGNED + ERFINV3_NUM_6
        num = (num * r) // ONE_SIGNED + ERFINV3_NUM_7
        
        denom: int256 = (ERFINV3_DEN_0 * r) // ONE_SIGNED + ERFINV3_DEN_1
        denom = (denom * r) // ONE_SIGNED + ERFINV3_DEN_2
        denom = (denom * r) // ONE_SIGNED + ERFINV3_DEN_3
        denom = (denom * r) // ONE_SIGNED + ERFINV3_DEN_4
        denom = (denom * r) // ONE_SIGNED + ERFINV3_DEN_5
        denom = (denom * r) // ONE_SIGNED + ERFINV3_DEN_6
        denom = (denom * r) // ONE_SIGNED + ERFINV3_DEN_7
        
        y = (num * ERFINV3_SCALE) // denom
    
    if x < 0:
        y = -y
    
    return y


@internal
@pure
def _erfcinv_internal(x: int256) -> int256:
    x_96: int256 = ((ONE_SIGNED - x) << POW) // ONE_SIGNED
    return self._erfinv_internal(x_96)


@external
@pure
def erfc(x: int256) -> uint256:
    return self._erfc_internal(x)


@external
@pure
def erfinv(x: int256) -> int256:
    return self._erfinv_internal(x)


@external
@pure
def erfcinv(x: int256) -> int256:
    return self._erfcinv_internal(x)


@external
@pure
def ppf(x: int256, u: int256, o: int256) -> int256:
    erfcinv_val: int256 = self._erfcinv_internal(2 * x)
    
    result: int256 = u - (o * SQRT2_WAD * erfcinv_val) // ONE_SQUARED
    
    return result


@external
@pure
def cdf(x: int256, u: int256, o: uint256) -> uint256:
    diff: int256 = u - x
    z: int256 = (diff * INV_SQRT2_96) // convert(o, int256)
    
    erfc_result: uint256 = self._erfc_internal(z)
    
    return erfc_result >> 1
