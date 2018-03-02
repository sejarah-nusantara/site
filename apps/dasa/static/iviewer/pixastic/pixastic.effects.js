Pixastic.Effects = (function() {

    function defaultOptions(options, defaults) {
        var O = {};
        for (var opt in defaults) {
            if (typeof options[opt] == "undefined") {
                O[opt] = defaults[opt];
            } else {
                O[opt] = options[opt];
            }
        }
        return O;
    }

    function clamp(val, min, max) {
        return Math.min(max, Math.max(min, val));
    }
    
    function convolve5x5(inData, outData, width, height, kernel, progress, alpha, invert, mono) {
        var idx, r, g, b, a,
            pyc, pyp, pyn, pypp, pynn,
            pxc, pxp, pxn, pxpp, pxnn,
            x, y,
            
            prog, lastProg = 0,
            n = width * height * 4,
            
            k00 = kernel[0][0], k01 = kernel[0][1], k02 = kernel[0][2], k03 = kernel[0][3], k04 = kernel[0][4],
            k10 = kernel[1][0], k11 = kernel[1][1], k12 = kernel[1][2], k13 = kernel[1][3], k14 = kernel[1][4],
            k20 = kernel[2][0], k21 = kernel[2][1], k22 = kernel[2][2], k23 = kernel[2][3], k24 = kernel[2][4],
            k30 = kernel[3][0], k31 = kernel[3][1], k32 = kernel[3][2], k33 = kernel[3][3], k34 = kernel[3][4],
            k40 = kernel[4][0], k41 = kernel[4][1], k42 = kernel[4][2], k43 = kernel[4][3], k44 = kernel[4][4],
            
            p00, p01, p02, p03, p04,
            p10, p11, p12, p13, p14,
            p20, p21, p22, p23, p24,
            p30, p31, p32, p33, p34,
            p40, p41, p42, p43, p44;
            
        for (y=0;y<height;++y) {
            pyc = y * width * 4;
            pyp = pyc - width * 4;
            pypp = pyc - width * 4 * 2;
            pyn = pyc + width * 4;
            pynn = pyc + width * 4 * 2;

            if (y < 1) pyp = pyc;
            if (y >= width-1) pyn = pyc;
            if (y < 2) pypp = pyp;
            if (y >= width-2) pynn = pyn;
            
            for (x=0;x<width;++x) {
                idx = (y * width + x) * 4;
                
                pxc = x * 4;
                pxp = pxc - 4;
                pxn = pxc + 4;
                pxpp = pxc - 8;
                pxnn = pxc + 8;
          
                if (x < 1) pxp = pxc;
                if (x >= width-1) pxn = pxc;
                if (x < 2) pxpp = pxp;
                if (x >= width-2) pxnn = pxn;
                
                p00 = pypp + pxpp;    p01 = pypp + pxp;    p02 = pypp + pxc;    p03 = pypp + pxn;    p04 = pypp + pxnn;
                p10 = pyp  + pxpp;    p11 = pyp  + pxp;    p12 = pyp  + pxc;    p13 = pyp  + pxn;    p14 = pyp  + pxnn;
                p20 = pyc  + pxpp;    p21 = pyc  + pxp;    p22 = pyc  + pxc;    p23 = pyc  + pxn;    p24 = pyc  + pxnn;
                p30 = pyn  + pxpp;    p31 = pyn  + pxp;    p32 = pyn  + pxc;    p33 = pyn  + pxn;    p34 = pyn  + pxnn;
                p40 = pynn + pxpp;    p41 = pynn + pxp;    p42 = pynn + pxc;    p43 = pynn + pxn;    p44 = pynn + pxnn;

                r = inData[p00] * k00 + inData[p01] * k01 + inData[p02] * k02 + inData[p03] * k04 + inData[p02] * k04
                  + inData[p10] * k10 + inData[p11] * k11 + inData[p12] * k12 + inData[p13] * k14 + inData[p12] * k14
                  + inData[p20] * k20 + inData[p21] * k21 + inData[p22] * k22 + inData[p23] * k24 + inData[p22] * k24
                  + inData[p30] * k30 + inData[p31] * k31 + inData[p32] * k32 + inData[p33] * k34 + inData[p32] * k34
                  + inData[p40] * k40 + inData[p41] * k41 + inData[p42] * k42 + inData[p43] * k44 + inData[p42] * k44;
                  
                g = inData[p00+1] * k00 + inData[p01+1] * k01 + inData[p02+1] * k02 + inData[p03+1] * k04 + inData[p02+1] * k04
                  + inData[p10+1] * k10 + inData[p11+1] * k11 + inData[p12+1] * k12 + inData[p13+1] * k14 + inData[p12+1] * k14
                  + inData[p20+1] * k20 + inData[p21+1] * k21 + inData[p22+1] * k22 + inData[p23+1] * k24 + inData[p22+1] * k24
                  + inData[p30+1] * k30 + inData[p31+1] * k31 + inData[p32+1] * k32 + inData[p33+1] * k34 + inData[p32+1] * k34
                  + inData[p40+1] * k40 + inData[p41+1] * k41 + inData[p42+1] * k42 + inData[p43+1] * k44 + inData[p42+1] * k44;
                  
                b = inData[p00+2] * k00 + inData[p01+2] * k01 + inData[p02+2] * k02 + inData[p03+2] * k04 + inData[p02+2] * k04
                  + inData[p10+2] * k10 + inData[p11+2] * k11 + inData[p12+2] * k12 + inData[p13+2] * k14 + inData[p12+2] * k14
                  + inData[p20+2] * k20 + inData[p21+2] * k21 + inData[p22+2] * k22 + inData[p23+2] * k24 + inData[p22+2] * k24
                  + inData[p30+2] * k30 + inData[p31+2] * k31 + inData[p32+2] * k32 + inData[p33+2] * k34 + inData[p32+2] * k34
                  + inData[p40+2] * k40 + inData[p41+2] * k41 + inData[p42+2] * k42 + inData[p43+2] * k44 + inData[p42+2] * k44;

                if (alpha) {
                    a = inData[p00+3] * k00 + inData[p01+3] * k01 + inData[p02+3] * k02 + inData[p03+3] * k04 + inData[p02+3] * k04
                      + inData[p10+3] * k10 + inData[p11+3] * k11 + inData[p12+3] * k12 + inData[p13+3] * k14 + inData[p12+3] * k14
                      + inData[p20+3] * k20 + inData[p21+3] * k21 + inData[p22+3] * k22 + inData[p23+3] * k24 + inData[p22+3] * k24
                      + inData[p30+3] * k30 + inData[p31+3] * k31 + inData[p32+3] * k32 + inData[p33+3] * k34 + inData[p32+3] * k34
                      + inData[p40+3] * k40 + inData[p41+3] * k41 + inData[p42+3] * k42 + inData[p43+3] * k44 + inData[p42+3] * k44;
                } else {
                    a = inData[idx+3];
                }

                if (mono) {
                    r = g = b = (r + g + b) / 3;
                }
                
                if (invert) {
                    r = 255 - r;
                    g = 255 - g;
                    b = 255 - b;
                }
                
                outData[idx] = r;
                outData[idx+1] = g;
                outData[idx+2] = b;
                outData[idx+3] = a;
                
                if (progress) {
                    prog = (idx/n*100 >> 0) / 100;
                    if (prog > lastProg) {
                        lastProg = progress(prog);
                    }
                }
            }
        }
    }
    
    function gaussian(inData, outData, width, height, kernelSize, progress) {
        var r, g, b, a, idx,
            n = width * height * 4,
            x, y, i, j, 
            inx, iny, w,
            maxKernelSize = 23,
            kernelSize = clamp(kernelSize, 3, maxKernelSize),
            k1 = -kernelSize / 2 + (kernelSize % 2 ? 0.5 : 0),
            k2 = kernelSize + k1,
            weights,
            kernels = [[1]],
            prog, lastProg = 0;
            
            
        for (i=1;i<maxKernelSize;++i) {
            kernels[0][i] = 0;
        }
        
        for (i=1;i<maxKernelSize;++i) {
            kernels[i] = [1];
            for (j=1;j<maxKernelSize;++j) {
                kernels[i][j] = kernels[i-1][j] + kernels[i-1][j-1];
            }
        }

        weights = kernels[kernelSize - 1]
        
        for (i=0,w=0;i<kernelSize;++i) {
            w += weights[i];
        }
        for (i=0;i<kernelSize;++i) {
            weights[i] /= w;
        }
        
        // pass 1
        for (y=0;y<height;++y) {
            for (x=0;x<width;++x) {
                r = g = b = a = 0;

                for (i=k1;i<k2;++i) {
                    inx = x + i;
                    iny = y;
                    w = weights[i - k1];
                    
                    if (inx < 0) {
                        inx = 0;
                    }
                    if (inx >= width) {
                        inx = width - 1;
                    }
                    
                    idx = (iny * width + inx) * 4;

                    r += inData[idx] * w;
                    g += inData[idx + 1] * w;
                    b += inData[idx + 2] * w;
                    a += inData[idx + 3] * w;

                }
                
                idx = (y * width + x) * 4;
                
                inData[idx] = r;
                inData[idx+1] = g;
                inData[idx+2] = b;
                inData[idx+3] = a;
                
                if (progress) {
                    prog = (idx/n*50 >> 0) / 100;
                    if (prog > lastProg) {
                        lastProg = progress(prog);
                    }
                }
            }
        }
        
        lastProg = 0;
        
        // pass 2
        for (y=0;y<height;++y) {
            for (x=0;x<width;++x) {
                r = g = b = a = 0;

                for (i=k1;i<k2;++i) {
                    inx = x;
                    iny = y + i;
                    w = weights[i - k1];
                    
                    if (iny < 0) {
                        iny = 0;
                    }
                    if (iny >= height) {
                        iny = height - 1;
                    }
                    
                    idx = (iny * width + inx) * 4;
                    
                    r += inData[idx] * w;
                    g += inData[idx + 1] * w;
                    b += inData[idx + 2] * w;
                    a += inData[idx + 3] * w;
                }
                
                idx = (y * width + x) * 4;
                
                outData[idx] = r;
                outData[idx+1] = g;
                outData[idx+2] = b;
                outData[idx+3] = a;
                
                if (progress) {
                    prog = 0.5 + (idx/n*50 >> 0) / 100;
                    if (prog > lastProg) {
                        lastProg = progress(prog);
                    }
                }
            }
        }
    }
    
    
    return {

    	brightness : function(inData, outData, width, height, options, progress) {
            options = defaultOptions(options, {
                brightness : 0,
                contrast : 0
            });
            
            var contrast = clamp(options.contrast, -1, 1) / 2,
                brightness = 1 + clamp(options.brightness, -1, 1),
                prog, lastProg = 0,
                r, g, b,
                n = width * height * 4;

            var brightMul = brightness < 0 ? - brightness : brightness;
            var brightAdd = brightness < 0 ? 0 : brightness;

            contrast = 0.5 * Math.tan((contrast + 1) * Math.PI/4);
            contrastAdd = - (contrast - 0.5) * 255;

            for (var i=0;i<n;i+=4) {
                r = inData[i];
                g = inData[i+1];
                b = inData[i+2];
                
                r = (r + r * brightMul + brightAdd) * contrast + contrastAdd;
                g = (g + g * brightMul + brightAdd) * contrast + contrastAdd;
                b = (b + b * brightMul + brightAdd) * contrast + contrastAdd;
                
                outData[i] = r;
                outData[i+1] = g;
                outData[i+2] = b;
                outData[i+3] = inData[i+3];
                
                if (progress) {
                    prog = (i/n*100 >> 0) / 100;
                    if (prog > lastProg) {
                        lastProg = progress(prog);
                    }
                }
            }
        },

        blur : function(inData, outData, width, height, options, progress) {
            gaussian(inData, outData, width, height, 3+Math.round(options.strength*20), progress);
        },

        // A 5x5 high-pass filter
        sharpen5x5 : function(inData, outData, width, height, options, progress) {
            var a = - clamp(options.strength, 0, 1);
            convolve5x5(
                inData, outData, width, height, 
                [[a, a,      a, a, a],
                 [a, a,      a, a, a],
                 [a, a, 1-a*24, a, a],
                 [a, a,      a, a, a],
                 [a, a,      a, a, a]],
                progress
             );
        },

        hsl : function(inData, outData, width, height, options, progress) {
            var n = width * height * 4,
                hue = clamp(options.hue, -1, 1),
                saturation = clamp(options.saturation, -1, 1),
                lightness = clamp(options.lightness, -1, 1),
                satMul = 1 + saturation * (saturation < 0 ? 1 : 2),
                lightMul = lightness < 0 ? 1 + lightness : 1 - lightness,
                lightAdd = lightness < 0 ? 0 : lightness * 255,
                vs, ms, vm, h, s, l, v, m, vmh, sextant,
                prog, lastProg = 0;

            hue = (hue * 6) % 6;
                    
            for (var i=0;i<n;i+=4) {

                r = inData[i];
                g = inData[i+1];
                b = inData[i+2];
                
                if (hue != 0 || saturation != 0) {
                    // ok, here comes rgb to hsl + adjust + hsl to rgb, all in one jumbled mess. 
                    // It's not so pretty, but it's been optimized to get somewhat decent performance.
                    // The transforms were originally adapted from the ones found in Graphics Gems, but have been heavily modified.
                    vs = r;
                    if (g > vs) vs = g;
                    if (b > vs) vs = b;
                    ms = r;
                    if (g < ms) ms = g;
                    if (b < ms) ms = b;
                    vm = (vs-ms);
                    l = (ms+vs)/510;
                    
                    if (l > 0 && vm > 0) {
                        if (l <= 0.5) {
                            s = vm / (vs+ms) * satMul;
                            if (s > 1) s = 1;
                            v = (l * (1+s));
                        } else {
                            s = vm / (510-vs-ms) * satMul;
                            if (s > 1) s = 1;
                            v = (l+s - l*s);
                        }
                        if (r == vs) {
                            if (g == ms) {
                                h = 5 + ((vs-b)/vm) + hue;
                            } else {
                                h = 1 - ((vs-g)/vm) + hue;
                            }
                        } else if (g == vs) {
                            if (b == ms) {
                                h = 1 + ((vs-r)/vm) + hue;
                            } else {
                                h = 3 - ((vs-b)/vm) + hue;
                            }
                        } else {
                            if (r == ms) {
                                h = 3 + ((vs-g)/vm) + hue;
                            } else {
                                h = 5 - ((vs-r)/vm) + hue;
                            }
                        }
                        if (h < 0) h += 6;
                        if (h >= 6) h -= 6;
                        m = (l + l - v);
                        sextant = h >> 0;
                        vmh = (v - m) * (h - sextant);
                        if (sextant == 0) {
                            r = v; 
                            g = m + vmh;
                            b = m;
                        } else if (sextant == 1) {
                            r = v - vmh;
                            g = v;
                            b = m;
                        } else if (sextant == 2) {
                            r = m;
                            g = v;
                            b = m + vmh;
                        } else if (sextant == 3) {
                            r = m;
                            g = v - vmh;
                            b = v;
                        } else if (sextant == 4) {
                            r = m + vmh;
                            g = m;
                            b = v;
                        } else if (sextant == 5) {
                            r = v;
                            g = m;
                            b = v - vmh;
                        }
                        
                        r *= 255;
                        g *= 255;
                        b *= 255;
                    }
                }
                
                r = r * lightMul + lightAdd;
                g = g * lightMul + lightAdd;
                b = b * lightMul + lightAdd;
                
                if (r < 0) r = 0;
                if (g < 0) g = 0;
                if (b < 0) b = 0;
                if (r > 255) r = 255;
                if (g > 255) g = 255;
                if (b > 255) b = 255;
                
                outData[i] = r;
                outData[i+1] = g;
                outData[i+2] = b;
                outData[i+3] = inData[i+3];
                
                if (progress) {
                    prog = (i/n*100 >> 0) / 100;
                    if (prog > lastProg) {
                        lastProg = progress(prog);
                    }
                }
            }
        }
        
    };

})();
