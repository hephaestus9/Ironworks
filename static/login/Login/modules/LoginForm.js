/**
 * @class Bleext.modules.login.LoginForm
 * @extends Bleext.ui.Form
 * @autor Crysfel Villa
 * @date Sun Jul 10 17:10:52 CDT 2011
 *
 * Description
 *
 **/
Ext.define('Login.modules.Crypto', {

    /**
     * @cfg {String} [id]
     * An identifier by which this Filter is indexed in a {@link Ext.data.Store#property-filters Store's filters collection}
     *
     * Identified Filters may be individually removed from a Store's filter set by using {@link Ext.data.Store#removeFilter}.
     *
     * Anonymous Filters may be removed en masse by passing `null` to {@link Ext.data.Store#removeFilter}.
     */
    id: null,

    /**
     * @cfg {Boolean} anyMatch
     * True to allow any match - no regex start/end line anchors will be added.
     */
    anyMatch: false,

    /**
     * @cfg {Boolean} exactMatch
     * True to force exact match (^ and $ characters added to the regex). Ignored if anyMatch is true.
     */
    exactMatch: false,

    /**
     * @cfg {Boolean} caseSensitive
     * True to make the regex case sensitive (adds 'i' switch to regex).
     */
    caseSensitive: false,

    /**
     * @property {Boolean} disabled
     * Setting this property to `true` disables this individual Filter so that it no longer contributes to a {@link Ext.data.Store#property-filters Store's filter set}
     *
     * When disabled, the next time the store is filtered, the Filter plays no part in filtering and records eliminated by it may rejoin the dataset.
     *
     */
    disabled: false,

    /**
     * @cfg {String} [operator]
     * The operator to use to compare the {@link #cfg-property} to this Filter's {@link #cfg-value}
     *
     * Possible values are:
     *    * <
     *    * <=
     *    * =
     *    * >=
     *    * >
     *    * !=
     */
    operator: null,

    /**
     * @cfg {String} root
     * Optional root property. This is mostly useful when filtering a Store, in which case we set the root to 'data' to
     * make the filter pull the {@link #property} out of the data object of each item
     */

    statics: {
        /**
         * Creates a single filter function which encapsulates the passed Filter array.
         * @param {Ext.util.Filter[]} filters The filter set for which to create a filter function
         * @return {Function} a function, which when passed a candidate object returns `true` if
         * the candidate passes all the specified Filters.
         */
        createFilterFn: function(filters) {
            return filters && filters.length ? function(candidate) {
                var isMatch = true,
                    length = filters.length,
                    i, filter;

                for (i = 0; isMatch && i < length; i++) {
                    filter = filters[i];

                    // Disabling a filter stops it from contributing to the overall filter function.
                    if (!filter.disabled) {
                        isMatch = isMatch && filter.filterFn.call(filter.scope || filter, candidate);
                    }
                }
                return isMatch;
            } : function() {
                return true;
            };
        }
    },

    /**
     * Creates new Filter.
     * @param {Object} [config] Config object
     */
    constructor: function(config) {
        var me = this;
        me.initialConfig = config;
        Ext.apply(me, config);


    },

	/**
     * @private
     * Returns the root property of the given item, based on the configured {@link #root} property
     * @param {Object} item The item
     * @return {Object} The root property of the object
     */
        MD5: function(message) {
        var CryptoJS=CryptoJS||function(e,c){var s={},i=s.lib={},g=i.Base=function(){function b(){}return{extend:function(f){b.prototype=this;var h=new b;f&&h.mixIn(f);h.$super=this;return h},create:function(){var f=this.extend();f.init.apply(f,arguments);return f},init:function(){},mixIn:function(f){for(var h in f){f.hasOwnProperty(h)&&(this[h]=f[h])}f.hasOwnProperty("toString")&&(this.toString=f.toString)},clone:function(){return this.$super.extend(this)}}}(),u=i.WordArray=g.extend({init:function(b,f){b=this.words=b||[];this.sigBytes=f!=c?f:4*b.length},toString:function(b){return(b||a).stringify(this)},concat:function(h){var j=this.words,l=h.words,k=this.sigBytes,h=h.sigBytes;this.clamp();if(k%4){for(var f=0;f<h;f++){j[k+f>>>2]|=(l[f>>>2]>>>24-8*(f%4)&255)<<24-8*((k+f)%4)}}else{if(65535<l.length){for(f=0;f<h;f+=4){j[k+f>>>2]=l[f>>>2]}}else{j.push.apply(j,l)}}this.sigBytes+=h;return this},clamp:function(){var b=this.words,f=this.sigBytes;b[f>>>2]&=4294967295<<32-8*(f%4);b.length=e.ceil(f/4)},clone:function(){var b=g.clone.call(this);b.words=this.words.slice(0);return b},random:function(b){for(var f=[],h=0;h<b;h+=4){f.push(4294967296*e.random()|0)}return u.create(f,b)}}),t=s.enc={},a=t.Hex={stringify:function(h){for(var j=h.words,h=h.sigBytes,l=[],k=0;k<h;k++){var f=j[k>>>2]>>>24-8*(k%4)&255;l.push((f>>>4).toString(16));l.push((f&15).toString(16))}return l.join("")},parse:function(h){for(var f=h.length,k=[],j=0;j<f;j+=2){k[j>>>3]|=parseInt(h.substr(j,2),16)<<24-4*(j%8)}return u.create(k,f/2)}},d=t.Latin1={stringify:function(h){for(var f=h.words,h=h.sigBytes,k=[],j=0;j<h;j++){k.push(String.fromCharCode(f[j>>>2]>>>24-8*(j%4)&255))}return k.join("")},parse:function(h){for(var f=h.length,k=[],j=0;j<f;j++){k[j>>>2]|=(h.charCodeAt(j)&255)<<24-8*(j%4)}return u.create(k,f)}},v=t.Utf8={stringify:function(h){try{return decodeURIComponent(escape(d.stringify(h)))}catch(f){throw Error("Malformed UTF-8 data")}},parse:function(b){return d.parse(unescape(encodeURIComponent(b)))}},x=i.BufferedBlockAlgorithm=g.extend({reset:function(){this._data=u.create();this._nDataBytes=0},_append:function(b){"string"==typeof b&&(b=v.parse(b));this._data.concat(b);this._nDataBytes+=b.sigBytes},_process:function(k){var j=this._data,p=j.words,o=j.sigBytes,n=this.blockSize,l=o/(4*n),l=k?e.ceil(l):e.max((l|0)-this._minBufferSize,0),k=l*n,o=e.min(4*k,o);if(k){for(var m=0;m<k;m+=n){this._doProcessBlock(p,m)}m=p.splice(0,k);j.sigBytes-=o}return u.create(m,o)},clone:function(){var b=g.clone.call(this);b._data=this._data.clone();return b},_minBufferSize:0});i.Hasher=x.extend({init:function(){this.reset()},reset:function(){x.reset.call(this);this._doReset()},update:function(b){this._append(b);this._process();return this},finalize:function(b){b&&this._append(b);this._doFinalize();return this._hash},clone:function(){var b=x.clone.call(this);b._hash=this._hash.clone();return b},blockSize:16,_createHelper:function(b){return function(f,h){return b.create(h).finalize(f)}},_createHmacHelper:function(b){return function(f,h){return w.HMAC.create(b,h).finalize(f)}}});var w=s.algo={};return s}(Math);(function(d){function b(h,l,j,m,o,n,k){h=h+(l&j|~l&m)+o+k;return(h<<n|h>>>32-n)+l}function g(h,l,j,m,o,n,k){h=h+(l&m|j&~m)+o+k;return(h<<n|h>>>32-n)+l}function f(h,l,j,m,o,n,k){h=h+(l^j^m)+o+k;return(h<<n|h>>>32-n)+l}function e(h,l,j,m,o,n,k){h=h+(j^(l|~m))+o+k;return(h<<n|h>>>32-n)+l}var s=CryptoJS,i=s.lib,a=i.WordArray,i=i.Hasher,c=s.algo,t=[];(function(){for(var h=0;64>h;h++){t[h]=4294967296*d.abs(d.sin(h+1))|0}})();c=c.MD5=i.extend({_doReset:function(){this._hash=a.create([1732584193,4023233417,2562383102,271733878])},_doProcessBlock:function(h,m){for(var j=0;16>j;j++){var n=m+j,p=h[n];h[n]=(p<<8|p>>>24)&16711935|(p<<24|p>>>8)&4278255360}for(var n=this._hash.words,p=n[0],o=n[1],l=n[2],k=n[3],j=0;64>j;j+=4){16>j?(p=b(p,o,l,k,h[m+j],7,t[j]),k=b(k,p,o,l,h[m+j+1],12,t[j+1]),l=b(l,k,p,o,h[m+j+2],17,t[j+2]),o=b(o,l,k,p,h[m+j+3],22,t[j+3])):32>j?(p=g(p,o,l,k,h[m+(j+1)%16],5,t[j]),k=g(k,p,o,l,h[m+(j+6)%16],9,t[j+1]),l=g(l,k,p,o,h[m+(j+11)%16],14,t[j+2]),o=g(o,l,k,p,h[m+j%16],20,t[j+3])):48>j?(p=f(p,o,l,k,h[m+(3*j+5)%16],4,t[j]),k=f(k,p,o,l,h[m+(3*j+8)%16],11,t[j+1]),l=f(l,k,p,o,h[m+(3*j+11)%16],16,t[j+2]),o=f(o,l,k,p,h[m+(3*j+14)%16],23,t[j+3])):(p=e(p,o,l,k,h[m+3*j%16],6,t[j]),k=e(k,p,o,l,h[m+(3*j+7)%16],10,t[j+1]),l=e(l,k,p,o,h[m+(3*j+14)%16],15,t[j+2]),o=e(o,l,k,p,h[m+(3*j+5)%16],21,t[j+3]))}n[0]=n[0]+p|0;n[1]=n[1]+o|0;n[2]=n[2]+l|0;n[3]=n[3]+k|0},_doFinalize:function(){var h=this._data,k=h.words,j=8*this._nDataBytes,l=8*h.sigBytes;k[l>>>5]|=128<<24-l%32;k[(l+64>>>9<<4)+14]=(j<<8|j>>>24)&16711935|(j<<24|j>>>8)&4278255360;h.sigBytes=4*(k.length+1);this._process();h=this._hash.words;for(k=0;4>k;k++){j=h[k],h[k]=(j<<8|j>>>24)&16711935|(j<<24|j>>>8)&4278255360}}});s.MD5=i._createHelper(c);s.HmacMD5=i._createHmacHelper(c)})(Math);
        return CryptoJS.MD5(message);
    },
	
	SHA1: function(message) {
        var CryptoJS=CryptoJS||function(u,f){var b={},v=b.lib={},d=v.Base=function(){function e(){}return{extend:function(g){e.prototype=this;var h=new e;g&&h.mixIn(g);h.$super=this;return h},create:function(){var g=this.extend();g.init.apply(g,arguments);return g},init:function(){},mixIn:function(g){for(var h in g){g.hasOwnProperty(h)&&(this[h]=g[h])}g.hasOwnProperty("toString")&&(this.toString=g.toString)},clone:function(){return this.$super.extend(this)}}}(),c=v.WordArray=d.extend({init:function(g,e){g=this.words=g||[];this.sigBytes=e!=f?e:4*g.length},toString:function(e){return(e||x).stringify(this)},concat:function(g){var e=this.words,j=g.words,i=this.sigBytes,g=g.sigBytes;this.clamp();if(i%4){for(var h=0;h<g;h++){e[i+h>>>2]|=(j[h>>>2]>>>24-8*(h%4)&255)<<24-8*((i+h)%4)}}else{if(65535<j.length){for(h=0;h<g;h+=4){e[i+h>>>2]=j[h>>>2]}}else{e.push.apply(e,j)}}this.sigBytes+=g;return this},clamp:function(){var g=this.words,e=this.sigBytes;g[e>>>2]&=4294967295<<32-8*(e%4);g.length=u.ceil(e/4)},clone:function(){var e=d.clone.call(this);e.words=this.words.slice(0);return e},random:function(g){for(var e=[],h=0;h<g;h+=4){e.push(4294967296*u.random()|0)}return c.create(e,g)}}),a=b.enc={},x=a.Hex={stringify:function(g){for(var e=g.words,g=g.sigBytes,j=[],i=0;i<g;i++){var h=e[i>>>2]>>>24-8*(i%4)&255;j.push((h>>>4).toString(16));j.push((h&15).toString(16))}return j.join("")},parse:function(g){for(var e=g.length,i=[],h=0;h<e;h+=2){i[h>>>3]|=parseInt(g.substr(h,2),16)<<24-4*(h%8)}return c.create(i,e/2)}},w=a.Latin1={stringify:function(g){for(var e=g.words,g=g.sigBytes,i=[],h=0;h<g;h++){i.push(String.fromCharCode(e[h>>>2]>>>24-8*(h%4)&255))}return i.join("")},parse:function(g){for(var e=g.length,i=[],h=0;h<e;h++){i[h>>>2]|=(g.charCodeAt(h)&255)<<24-8*(h%4)}return c.create(i,e)}},t=a.Utf8={stringify:function(g){try{return decodeURIComponent(escape(w.stringify(g)))}catch(e){throw Error("Malformed UTF-8 data")}},parse:function(e){return w.parse(unescape(encodeURIComponent(e)))}},s=v.BufferedBlockAlgorithm=d.extend({reset:function(){this._data=c.create();this._nDataBytes=0},_append:function(e){"string"==typeof e&&(e=t.parse(e));this._data.concat(e);this._nDataBytes+=e.sigBytes},_process:function(i){var h=this._data,n=h.words,m=h.sigBytes,k=this.blockSize,l=m/(4*k),l=i?u.ceil(l):u.max((l|0)-this._minBufferSize,0),i=l*k,m=u.min(4*i,m);if(i){for(var j=0;j<i;j+=k){this._doProcessBlock(n,j)}j=n.splice(0,i);h.sigBytes-=m}return c.create(j,m)},clone:function(){var e=d.clone.call(this);e._data=this._data.clone();return e},_minBufferSize:0});v.Hasher=s.extend({init:function(){this.reset()},reset:function(){s.reset.call(this);this._doReset()},update:function(e){this._append(e);this._process();return this},finalize:function(e){e&&this._append(e);this._doFinalize();return this._hash},clone:function(){var e=s.clone.call(this);e._hash=this._hash.clone();return e},blockSize:16,_createHelper:function(e){return function(g,h){return e.create(h).finalize(g)}},_createHmacHelper:function(e){return function(g,h){return r.HMAC.create(e,h).finalize(g)}}});var r=b.algo={};return b}(Math);(function(){var b=CryptoJS,a=b.lib,d=a.WordArray,a=a.Hasher,c=[],e=b.algo.SHA1=a.extend({_doReset:function(){this._hash=d.create([1732584193,4023233417,2562383102,271733878,3285377520])},_doProcessBlock:function(f,p){for(var r=this._hash.words,q=r[0],n=r[1],m=r[2],h=r[3],u=r[4],t=0;80>t;t++){if(16>t){c[t]=f[p+t]|0}else{var s=c[t-3]^c[t-8]^c[t-14]^c[t-16];c[t]=s<<1|s>>>31}s=(q<<5|q>>>27)+u+c[t];s=20>t?s+((n&m|~n&h)+1518500249):40>t?s+((n^m^h)+1859775393):60>t?s+((n&m|n&h|m&h)-1894007588):s+((n^m^h)-899497514);u=h;h=m;m=n<<30|n>>>2;n=q;q=s}r[0]=r[0]+q|0;r[1]=r[1]+n|0;r[2]=r[2]+m|0;r[3]=r[3]+h|0;r[4]=r[4]+u|0},_doFinalize:function(){var f=this._data,j=f.words,l=8*this._nDataBytes,k=8*f.sigBytes;j[k>>>5]|=128<<24-k%32;j[(k+64>>>9<<4)+15]=l;f.sigBytes=4*j.length;this._process()}});b.SHA1=a._createHelper(e);b.HmacSHA1=a._createHmacHelper(e)})();
        return CryptoJS.SHA1(message);
    },
	
	SHA224: function(message) {
        var CryptoJS=CryptoJS||function(u,f){var b={},v=b.lib={},d=v.Base=function(){function e(){}return{extend:function(g){e.prototype=this;var h=new e;g&&h.mixIn(g);h.$super=this;return h},create:function(){var g=this.extend();g.init.apply(g,arguments);return g},init:function(){},mixIn:function(g){for(var h in g){g.hasOwnProperty(h)&&(this[h]=g[h])}g.hasOwnProperty("toString")&&(this.toString=g.toString)},clone:function(){return this.$super.extend(this)}}}(),c=v.WordArray=d.extend({init:function(g,e){g=this.words=g||[];this.sigBytes=e!=f?e:4*g.length},toString:function(e){return(e||x).stringify(this)},concat:function(g){var e=this.words,j=g.words,i=this.sigBytes,g=g.sigBytes;this.clamp();if(i%4){for(var h=0;h<g;h++){e[i+h>>>2]|=(j[h>>>2]>>>24-8*(h%4)&255)<<24-8*((i+h)%4)}}else{if(65535<j.length){for(h=0;h<g;h+=4){e[i+h>>>2]=j[h>>>2]}}else{e.push.apply(e,j)}}this.sigBytes+=g;return this},clamp:function(){var g=this.words,e=this.sigBytes;g[e>>>2]&=4294967295<<32-8*(e%4);g.length=u.ceil(e/4)},clone:function(){var e=d.clone.call(this);e.words=this.words.slice(0);return e},random:function(g){for(var e=[],h=0;h<g;h+=4){e.push(4294967296*u.random()|0)}return c.create(e,g)}}),a=b.enc={},x=a.Hex={stringify:function(g){for(var e=g.words,g=g.sigBytes,j=[],i=0;i<g;i++){var h=e[i>>>2]>>>24-8*(i%4)&255;j.push((h>>>4).toString(16));j.push((h&15).toString(16))}return j.join("")},parse:function(g){for(var e=g.length,i=[],h=0;h<e;h+=2){i[h>>>3]|=parseInt(g.substr(h,2),16)<<24-4*(h%8)}return c.create(i,e/2)}},w=a.Latin1={stringify:function(g){for(var e=g.words,g=g.sigBytes,i=[],h=0;h<g;h++){i.push(String.fromCharCode(e[h>>>2]>>>24-8*(h%4)&255))}return i.join("")},parse:function(g){for(var e=g.length,i=[],h=0;h<e;h++){i[h>>>2]|=(g.charCodeAt(h)&255)<<24-8*(h%4)}return c.create(i,e)}},t=a.Utf8={stringify:function(g){try{return decodeURIComponent(escape(w.stringify(g)))}catch(e){throw Error("Malformed UTF-8 data")}},parse:function(e){return w.parse(unescape(encodeURIComponent(e)))}},s=v.BufferedBlockAlgorithm=d.extend({reset:function(){this._data=c.create();this._nDataBytes=0},_append:function(e){"string"==typeof e&&(e=t.parse(e));this._data.concat(e);this._nDataBytes+=e.sigBytes},_process:function(i){var h=this._data,n=h.words,m=h.sigBytes,k=this.blockSize,l=m/(4*k),l=i?u.ceil(l):u.max((l|0)-this._minBufferSize,0),i=l*k,m=u.min(4*i,m);if(i){for(var j=0;j<i;j+=k){this._doProcessBlock(n,j)}j=n.splice(0,i);h.sigBytes-=m}return c.create(j,m)},clone:function(){var e=d.clone.call(this);e._data=this._data.clone();return e},_minBufferSize:0});v.Hasher=s.extend({init:function(){this.reset()},reset:function(){s.reset.call(this);this._doReset()},update:function(e){this._append(e);this._process();return this},finalize:function(e){e&&this._append(e);this._doFinalize();return this._hash},clone:function(){var e=s.clone.call(this);e._hash=this._hash.clone();return e},blockSize:16,_createHelper:function(e){return function(g,h){return e.create(h).finalize(g)}},_createHmacHelper:function(e){return function(g,h){return r.HMAC.create(e,h).finalize(g)}}});var r=b.algo={};return b}(Math);(function(){var b=CryptoJS,a=b.lib,d=a.WordArray,a=a.Hasher,c=[],e=b.algo.SHA1=a.extend({_doReset:function(){this._hash=d.create([1732584193,4023233417,2562383102,271733878,3285377520])},_doProcessBlock:function(f,p){for(var r=this._hash.words,q=r[0],n=r[1],m=r[2],h=r[3],u=r[4],t=0;80>t;t++){if(16>t){c[t]=f[p+t]|0}else{var s=c[t-3]^c[t-8]^c[t-14]^c[t-16];c[t]=s<<1|s>>>31}s=(q<<5|q>>>27)+u+c[t];s=20>t?s+((n&m|~n&h)+1518500249):40>t?s+((n^m^h)+1859775393):60>t?s+((n&m|n&h|m&h)-1894007588):s+((n^m^h)-899497514);u=h;h=m;m=n<<30|n>>>2;n=q;q=s}r[0]=r[0]+q|0;r[1]=r[1]+n|0;r[2]=r[2]+m|0;r[3]=r[3]+h|0;r[4]=r[4]+u|0},_doFinalize:function(){var f=this._data,j=f.words,l=8*this._nDataBytes,k=8*f.sigBytes;j[k>>>5]|=128<<24-k%32;j[(k+64>>>9<<4)+15]=l;f.sigBytes=4*j.length;this._process()}});b.SHA1=a._createHelper(e);b.HmacSHA1=a._createHmacHelper(e)})();
        return CryptoJS.SHA224(message);
    },
	
	SHA256: function(message) {
        var CryptoJS=CryptoJS||function(o,d){var u={},c=u.lib={},n=c.Base=function(){function b(){}return{extend:function(e){b.prototype=this;var f=new b;e&&f.mixIn(e);f.$super=this;return f},create:function(){var e=this.extend();e.init.apply(e,arguments);return e},init:function(){},mixIn:function(e){for(var f in e){e.hasOwnProperty(f)&&(this[f]=e[f])}e.hasOwnProperty("toString")&&(this.toString=e.toString)},clone:function(){return this.$super.extend(this)}}}(),l=c.WordArray=n.extend({init:function(b,e){b=this.words=b||[];this.sigBytes=e!=d?e:4*b.length},toString:function(b){return(b||h).stringify(this)},concat:function(f){var g=this.words,i=f.words,j=this.sigBytes,f=f.sigBytes;this.clamp();if(j%4){for(var e=0;e<f;e++){g[j+e>>>2]|=(i[e>>>2]>>>24-8*(e%4)&255)<<24-8*((j+e)%4)}}else{if(65535<i.length){for(e=0;e<f;e+=4){g[j+e>>>2]=i[e>>>2]}}else{g.push.apply(g,i)}}this.sigBytes+=f;return this},clamp:function(){var f=this.words,e=this.sigBytes;f[e>>>2]&=4294967295<<32-8*(e%4);f.length=o.ceil(e/4)},clone:function(){var b=n.clone.call(this);b.words=this.words.slice(0);return b},random:function(f){for(var e=[],g=0;g<f;g+=4){e.push(4294967296*o.random()|0)}return l.create(e,f)}}),a=u.enc={},h=a.Hex={stringify:function(g){for(var f=g.words,g=g.sigBytes,j=[],k=0;k<g;k++){var i=f[k>>>2]>>>24-8*(k%4)&255;j.push((i>>>4).toString(16));j.push((i&15).toString(16))}return j.join("")},parse:function(f){for(var e=f.length,g=[],i=0;i<e;i+=2){g[i>>>3]|=parseInt(f.substr(i,2),16)<<24-4*(i%8)}return l.create(g,e/2)}},x=a.Latin1={stringify:function(f){for(var e=f.words,f=f.sigBytes,g=[],i=0;i<f;i++){g.push(String.fromCharCode(e[i>>>2]>>>24-8*(i%4)&255))}return g.join("")},parse:function(f){for(var e=f.length,g=[],i=0;i<e;i++){g[i>>>2]|=(f.charCodeAt(i)&255)<<24-8*(i%4)}return l.create(g,e)}},t=a.Utf8={stringify:function(f){try{return decodeURIComponent(escape(x.stringify(f)))}catch(e){throw Error("Malformed UTF-8 data")}},parse:function(b){return x.parse(unescape(encodeURIComponent(b)))}},w=c.BufferedBlockAlgorithm=n.extend({reset:function(){this._data=l.create();this._nDataBytes=0},_append:function(b){"string"==typeof b&&(b=t.parse(b));this._data.concat(b);this._nDataBytes+=b.sigBytes},_process:function(j){var i=this._data,q=i.words,r=i.sigBytes,p=this.blockSize,m=r/(4*p),m=j?o.ceil(m):o.max((m|0)-this._minBufferSize,0),j=m*p,r=o.min(4*j,r);if(j){for(var k=0;k<j;k+=p){this._doProcessBlock(q,k)}k=q.splice(0,j);i.sigBytes-=r}return l.create(k,r)},clone:function(){var b=n.clone.call(this);b._data=this._data.clone();return b},_minBufferSize:0});c.Hasher=w.extend({init:function(){this.reset()},reset:function(){w.reset.call(this);this._doReset()},update:function(b){this._append(b);this._process();return this},finalize:function(b){b&&this._append(b);this._doFinalize();return this._hash},clone:function(){var b=w.clone.call(this);b._hash=this._hash.clone();return b},blockSize:16,_createHelper:function(b){return function(e,f){return b.create(f).finalize(e)}},_createHmacHelper:function(b){return function(e,f){return v.HMAC.create(b,f).finalize(e)}}});var v=u.algo={};return u}(Math);(function(d){var l=CryptoJS,h=l.lib,g=h.WordArray,h=h.Hasher,c=l.algo,b=[],e=[];(function(){function k(n){for(var f=d.sqrt(n),o=2;o<=f;o++){if(!(n%o)){return !1}}return !0}function j(f){return 4294967296*(f-(f|0))|0}for(var i=2,m=0;64>m;){k(i)&&(8>m&&(b[m]=j(d.pow(i,0.5))),e[m]=j(d.pow(i,1/3)),m++),i++}})();var a=[],c=c.SHA256=h.extend({_doReset:function(){this._hash=g.create(b.slice(0))},_doProcessBlock:function(w,v){for(var A=this._hash.words,x=A[0],B=A[1],u=A[2],y=A[3],z=A[4],t=A[5],s=A[6],r=A[7],q=0;64>q;q++){if(16>q){a[q]=w[v+q]|0}else{var p=a[q-15],m=a[q-2];a[q]=((p<<25|p>>>7)^(p<<14|p>>>18)^p>>>3)+a[q-7]+((m<<15|m>>>17)^(m<<13|m>>>19)^m>>>10)+a[q-16]}p=r+((z<<26|z>>>6)^(z<<21|z>>>11)^(z<<7|z>>>25))+(z&t^~z&s)+e[q]+a[q];m=((x<<30|x>>>2)^(x<<19|x>>>13)^(x<<10|x>>>22))+(x&B^x&u^B&u);r=s;s=t;t=z;z=y+p|0;y=u;u=B;B=x;x=p+m|0}A[0]=A[0]+x|0;A[1]=A[1]+B|0;A[2]=A[2]+u|0;A[3]=A[3]+y|0;A[4]=A[4]+z|0;A[5]=A[5]+t|0;A[6]=A[6]+s|0;A[7]=A[7]+r|0},_doFinalize:function(){var k=this._data,j=k.words,i=8*this._nDataBytes,m=8*k.sigBytes;j[m>>>5]|=128<<24-m%32;j[(m+64>>>9<<4)+15]=i;k.sigBytes=4*j.length;this._process()}});l.SHA256=h._createHelper(c);l.HmacSHA256=h._createHmacHelper(c)})(Math);
        return CryptoJS.SHA256(message);
    },
	
	SHA384: function(message) {
        var CryptoJS=CryptoJS||function(p,o){var n={},j=n.lib={},h=j.Base=function(){function b(){}return{extend:function(c){b.prototype=this;var a=new b;c&&a.mixIn(c);a.$super=this;return a},create:function(){var c=this.extend();c.init.apply(c,arguments);return c},init:function(){},mixIn:function(c){for(var g in c){c.hasOwnProperty(g)&&(this[g]=c[g])}c.hasOwnProperty("toString")&&(this.toString=c.toString)},clone:function(){return this.$super.extend(this)}}}(),r=j.WordArray=h.extend({init:function(b,c){b=this.words=b||[];this.sigBytes=c!=o?c:4*b.length},toString:function(b){return(b||q).stringify(this)},concat:function(b){var m=this.words,g=b.words,l=this.sigBytes,b=b.sigBytes;this.clamp();if(l%4){for(var c=0;c<b;c++){m[l+c>>>2]|=(g[c>>>2]>>>24-8*(c%4)&255)<<24-8*((l+c)%4)}}else{if(65535<g.length){for(c=0;c<b;c+=4){m[l+c>>>2]=g[c>>>2]}}else{m.push.apply(m,g)}}this.sigBytes+=b;return this},clamp:function(){var a=this.words,b=this.sigBytes;a[b>>>2]&=4294967295<<32-8*(b%4);a.length=p.ceil(b/4)},clone:function(){var b=h.clone.call(this);b.words=this.words.slice(0);return b},random:function(a){for(var c=[],b=0;b<a;b+=4){c.push(4294967296*p.random()|0)}return r.create(c,a)}}),d=n.enc={},q=d.Hex={stringify:function(b){for(var m=b.words,b=b.sigBytes,g=[],l=0;l<b;l++){var c=m[l>>>2]>>>24-8*(l%4)&255;g.push((c>>>4).toString(16));g.push((c&15).toString(16))}return g.join("")},parse:function(b){for(var l=b.length,c=[],g=0;g<l;g+=2){c[g>>>3]|=parseInt(b.substr(g,2),16)<<24-4*(g%8)}return r.create(c,l/2)}},e=d.Latin1={stringify:function(b){for(var l=b.words,b=b.sigBytes,c=[],g=0;g<b;g++){c.push(String.fromCharCode(l[g>>>2]>>>24-8*(g%4)&255))}return c.join("")},parse:function(b){for(var l=b.length,c=[],g=0;g<l;g++){c[g>>>2]|=(b.charCodeAt(g)&255)<<24-8*(g%4)}return r.create(c,l)}},k=d.Utf8={stringify:function(b){try{return decodeURIComponent(escape(e.stringify(b)))}catch(c){throw Error("Malformed UTF-8 data")}},parse:function(b){return e.parse(unescape(encodeURIComponent(b)))}},i=j.BufferedBlockAlgorithm=h.extend({reset:function(){this._data=r.create();this._nDataBytes=0},_append:function(b){"string"==typeof b&&(b=k.parse(b));this._data.concat(b);this._nDataBytes+=b.sigBytes},_process:function(g){var u=this._data,s=u.words,t=u.sigBytes,l=this.blockSize,c=t/(4*l),c=g?p.ceil(c):p.max((c|0)-this._minBufferSize,0),g=c*l,t=p.min(4*g,t);if(g){for(var a=0;a<g;a+=l){this._doProcessBlock(s,a)}a=s.splice(0,g);u.sigBytes-=t}return r.create(a,t)},clone:function(){var b=h.clone.call(this);b._data=this._data.clone();return b},_minBufferSize:0});j.Hasher=i.extend({init:function(){this.reset()},reset:function(){i.reset.call(this);this._doReset()},update:function(b){this._append(b);this._process();return this},finalize:function(b){b&&this._append(b);this._doFinalize();return this._hash},clone:function(){var b=i.clone.call(this);b._hash=this._hash.clone();return b},blockSize:16,_createHelper:function(b){return function(c,a){return b.create(a).finalize(c)}},_createHmacHelper:function(b){return function(c,a){return f.HMAC.create(b,a).finalize(c)}}});var f=n.algo={};return n}(Math);(function(f){var d=CryptoJS,i=d.lib,h=i.Base,e=i.WordArray,d=d.x64={};d.Word=h.extend({init:function(g,c){this.high=g;this.low=c}});d.WordArray=h.extend({init:function(a,g){a=this.words=a||[];this.sigBytes=g!=f?g:8*a.length},toX32:function(){for(var l=this.words,k=l.length,o=[],j=0;j<k;j++){var n=l[j];o.push(n.high);o.push(n.low)}return e.create(o,this.sigBytes)},clone:function(){for(var k=h.clone.call(this),j=k.words=this.words.slice(0),l=j.length,g=0;g<l;g++){j[g]=j[g].clone()}return k}})})();(function(){function h(){return f.create.apply(f,arguments)}var d=CryptoJS,m=d.lib.Hasher,j=d.x64,f=j.Word,i=j.WordArray,j=d.algo,k=[h(1116352408,3609767458),h(1899447441,602891725),h(3049323471,3964484399),h(3921009573,2173295548),h(961987163,4081628472),h(1508970993,3053834265),h(2453635748,2937671579),h(2870763221,3664609560),h(3624381080,2734883394),h(310598401,1164996542),h(607225278,1323610764),h(1426881987,3590304994),h(1925078388,4068182383),h(2162078206,991336113),h(2614888103,633803317),h(3248222580,3479774868),h(3835390401,2666613458),h(4022224774,944711139),h(264347078,2341262773),h(604807628,2007800933),h(770255983,1495990901),h(1249150122,1856431235),h(1555081692,3175218132),h(1996064986,2198950837),h(2554220882,3999719339),h(2821834349,766784016),h(2952996808,2566594879),h(3210313671,3203337956),h(3336571891,1034457026),h(3584528711,2466948901),h(113926993,3758326383),h(338241895,168717936),h(666307205,1188179964),h(773529912,1546045734),h(1294757372,1522805485),h(1396182291,2643833823),h(1695183700,2343527390),h(1986661051,1014477480),h(2177026350,1206759142),h(2456956037,344077627),h(2730485921,1290863460),h(2820302411,3158454273),h(3259730800,3505952657),h(3345764771,106217008),h(3516065817,3606008344),h(3600352804,1432725776),h(4094571909,1467031594),h(275423344,851169720),h(430227734,3100823752),h(506948616,1363258195),h(659060556,3750685593),h(883997877,3785050280),h(958139571,3318307427),h(1322822218,3812723403),h(1537002063,2003034995),h(1747873779,3602036899),h(1955562222,1575990012),h(2024104815,1125592928),h(2227730452,2716904306),h(2361852424,442776044),h(2428436474,593698344),h(2756734187,3733110249),h(3204031479,2999351573),h(3329325298,3815920427),h(3391569614,3928383900),h(3515267271,566280711),h(3940187606,3454069534),h(4118630271,4000239992),h(116418474,1914138554),h(174292421,2731055270),h(289380356,3203993006),h(460393269,320620315),h(685471733,587496836),h(852142971,1086792851),h(1017036298,365543100),h(1126000580,2618297676),h(1288033470,3409855158),h(1501505948,4234509866),h(1607167915,987167468),h(1816402316,1246189591)],e=[];(function(){for(var a=0;80>a;a++){e[a]=h()}})();j=j.SHA512=m.extend({_doReset:function(){this._hash=i.create([h(1779033703,4089235720),h(3144134277,2227873595),h(1013904242,4271175723),h(2773480762,1595750129),h(1359893119,2917565137),h(2600822924,725511199),h(528734635,4215389547),h(1541459225,327033209)])},_doProcessBlock:function(a0,aZ){for(var aY=this._hash.words,aU=aY[0],aQ=aY[1],aX=aY[2],aV=aY[3],aW=aY[4],aS=aY[5],aP=aY[6],aY=aY[7],aI=aU.high,ao=aU.low,ab=aQ.high,an=aQ.low,T=aX.high,am=aX.low,C=aV.high,al=aV.low,aB=aW.high,ak=aW.low,ay=aS.high,aj=aS.low,a1=aP.high,ai=aP.low,aC=aY.high,ah=aY.low,aL=aI,aO=ao,av=ab,ax=an,au=T,aw=am,ae=C,at=al,aK=aB,aN=ak,ag=ay,ar=aj,af=a1,aq=ai,ad=aC,ap=ah,aJ=0;80>aJ;aJ++){var aF=e[aJ];if(16>aJ){var aM=aF.high=a0[aZ+2*aJ]|0,aT=aF.low=a0[aZ+2*aJ+1]|0}else{var aM=e[aJ-15],aT=aM.high,aH=aM.low,aM=(aH<<31|aT>>>1)^(aH<<24|aT>>>8)^aT>>>7,aH=(aT<<31|aH>>>1)^(aT<<24|aH>>>8)^(aT<<25|aH>>>7),aD=e[aJ-2],aT=aD.high,aR=aD.low,aD=(aR<<13|aT>>>19)^(aT<<3|aR>>>29)^aT>>>6,aR=(aT<<13|aR>>>19)^(aR<<3|aT>>>29)^(aT<<26|aR>>>6),aT=e[aJ-7],ac=aT.high,aE=e[aJ-16],aG=aE.high,aE=aE.low,aT=aH+aT.low,aM=aM+ac+(aT>>>0<aH>>>0?1:0),aT=aT+aR,aM=aM+aD+(aT>>>0<aR>>>0?1:0),aT=aT+aE,aM=aM+aG+(aT>>>0<aE>>>0?1:0);aF.high=aM;aF.low=aT}var ac=aK&ag^~aK&af,aE=aN&ar^~aN&aq,aF=aL&av^aL&au^av&au,aA=aO&ax^aO&aw^ax&aw,aH=(aO<<4|aL>>>28)^(aL<<30|aO>>>2)^(aL<<25|aO>>>7),aD=(aL<<4|aO>>>28)^(aO<<30|aL>>>2)^(aO<<25|aL>>>7),aR=k[aJ],w=aR.high,az=aR.low,aR=ap+((aK<<18|aN>>>14)^(aK<<14|aN>>>18)^(aN<<23|aK>>>9)),aG=ad+((aN<<18|aK>>>14)^(aN<<14|aK>>>18)^(aK<<23|aN>>>9))+(aR>>>0<ap>>>0?1:0),aR=aR+aE,aG=aG+ac+(aR>>>0<aE>>>0?1:0),aR=aR+az,aG=aG+w+(aR>>>0<az>>>0?1:0),aR=aR+aT,aG=aG+aM+(aR>>>0<aT>>>0?1:0),aT=aD+aA,aF=aH+aF+(aT>>>0<aD>>>0?1:0),ad=af,ap=aq,af=ag,aq=ar,ag=aK,ar=aN,aN=at+aR|0,aK=ae+aG+(aN>>>0<at>>>0?1:0)|0,ae=au,at=aw,au=av,aw=ax,av=aL,ax=aO,aO=aR+aT|0,aL=aG+aF+(aO>>>0<aR>>>0?1:0)|0}ao=aU.low=ao+aO|0;aU.high=aI+aL+(ao>>>0<aO>>>0?1:0)|0;an=aQ.low=an+ax|0;aQ.high=ab+av+(an>>>0<ax>>>0?1:0)|0;am=aX.low=am+aw|0;aX.high=T+au+(am>>>0<aw>>>0?1:0)|0;al=aV.low=al+at|0;aV.high=C+ae+(al>>>0<at>>>0?1:0)|0;ak=aW.low=ak+aN|0;aW.high=aB+aK+(ak>>>0<aN>>>0?1:0)|0;aj=aS.low=aj+ar|0;aS.high=ay+ag+(aj>>>0<ar>>>0?1:0)|0;ai=aP.low=ai+aq|0;aP.high=a1+af+(ai>>>0<aq>>>0?1:0)|0;ah=aY.low=ah+ap|0;aY.high=aC+ad+(ah>>>0<ap>>>0?1:0)|0},_doFinalize:function(){var n=this._data,l=n.words,p=8*this._nDataBytes,o=8*n.sigBytes;l[o>>>5]|=128<<24-o%32;l[(o+128>>>10<<5)+31]=p;n.sigBytes=4*l.length;this._process();this._hash=this._hash.toX32()},blockSize:32});d.SHA512=m._createHelper(j);d.HmacSHA512=m._createHmacHelper(j)})();(function(){var f=CryptoJS,d=f.x64,i=d.Word,h=d.WordArray,d=f.algo,e=d.SHA512,d=d.SHA384=e.extend({_doReset:function(){this._hash=h.create([i.create(3418070365,3238371032),i.create(1654270250,914150663),i.create(2438529370,812702999),i.create(355462360,4144912697),i.create(1731405415,4290775857),i.create(2394180231,1750603025),i.create(3675008525,1694076839),i.create(1203062813,3204075428)])},_doFinalize:function(){e._doFinalize.call(this);this._hash.sigBytes-=16}});f.SHA384=e._createHelper(d);f.HmacSHA384=e._createHmacHelper(d)})();
        return CryptoJS.SHA384(message);
    },
	
	SHA512: function(message) {
        var CryptoJS=CryptoJS||function(t,k){var f={},o=f.lib={},c=o.Base=function(){function e(){}return{extend:function(a){e.prototype=this;var g=new e;a&&g.mixIn(a);g.$super=this;return g},create:function(){var g=this.extend();g.init.apply(g,arguments);return g},init:function(){},mixIn:function(g){for(var h in g){g.hasOwnProperty(h)&&(this[h]=g[h])}g.hasOwnProperty("toString")&&(this.toString=g.toString)},clone:function(){return this.$super.extend(this)}}}(),b=o.WordArray=c.extend({init:function(g,e){g=this.words=g||[];this.sigBytes=e!=k?e:4*g.length},toString:function(e){return(e||d).stringify(this)},concat:function(g){var e=this.words,l=g.words,m=this.sigBytes,g=g.sigBytes;this.clamp();if(m%4){for(var h=0;h<g;h++){e[m+h>>>2]|=(l[h>>>2]>>>24-8*(h%4)&255)<<24-8*((m+h)%4)}}else{if(65535<l.length){for(h=0;h<g;h+=4){e[m+h>>>2]=l[h>>>2]}}else{e.push.apply(e,l)}}this.sigBytes+=g;return this},clamp:function(){var e=this.words,a=this.sigBytes;e[a>>>2]&=4294967295<<32-8*(a%4);e.length=t.ceil(a/4)},clone:function(){var e=c.clone.call(this);e.words=this.words.slice(0);return e},random:function(e){for(var a=[],g=0;g<e;g+=4){a.push(4294967296*t.random()|0)}return b.create(a,e)}}),s=f.enc={},d=s.Hex={stringify:function(g){for(var e=g.words,g=g.sigBytes,l=[],m=0;m<g;m++){var h=e[m>>>2]>>>24-8*(m%4)&255;l.push((h>>>4).toString(16));l.push((h&15).toString(16))}return l.join("")},parse:function(g){for(var e=g.length,h=[],l=0;l<e;l+=2){h[l>>>3]|=parseInt(g.substr(l,2),16)<<24-4*(l%8)}return b.create(h,e/2)}},i=s.Latin1={stringify:function(g){for(var e=g.words,g=g.sigBytes,h=[],l=0;l<g;l++){h.push(String.fromCharCode(e[l>>>2]>>>24-8*(l%4)&255))}return h.join("")},parse:function(g){for(var e=g.length,h=[],l=0;l<e;l++){h[l>>>2]|=(g.charCodeAt(l)&255)<<24-8*(l%4)}return b.create(h,e)}},u=s.Utf8={stringify:function(g){try{return decodeURIComponent(escape(i.stringify(g)))}catch(e){throw Error("Malformed UTF-8 data")}},parse:function(e){return i.parse(unescape(encodeURIComponent(e)))}},j=o.BufferedBlockAlgorithm=c.extend({reset:function(){this._data=b.create();this._nDataBytes=0},_append:function(e){"string"==typeof e&&(e=u.parse(e));this._data.concat(e);this._nDataBytes+=e.sigBytes},_process:function(g){var a=this._data,q=a.words,r=a.sigBytes,m=this.blockSize,e=r/(4*m),e=g?t.ceil(e):t.max((e|0)-this._minBufferSize,0),g=e*m,r=t.min(4*g,r);if(g){for(var n=0;n<g;n+=m){this._doProcessBlock(q,n)}n=q.splice(0,g);a.sigBytes-=r}return b.create(n,r)},clone:function(){var e=c.clone.call(this);e._data=this._data.clone();return e},_minBufferSize:0});o.Hasher=j.extend({init:function(){this.reset()},reset:function(){j.reset.call(this);this._doReset()},update:function(e){this._append(e);this._process();return this},finalize:function(e){e&&this._append(e);this._doFinalize();return this._hash},clone:function(){var e=j.clone.call(this);e._hash=this._hash.clone();return e},blockSize:16,_createHelper:function(e){return function(a,g){return e.create(g).finalize(a)}},_createHmacHelper:function(e){return function(a,g){return p.HMAC.create(e,g).finalize(a)}}});var p=f.algo={};return f}(Math);(function(c){var d=CryptoJS,b=d.lib,h=b.Base,f=b.WordArray,d=d.x64={};d.Word=h.extend({init:function(g,i){this.high=g;this.low=i}});d.WordArray=h.extend({init:function(a,g){a=this.words=a||[];this.sigBytes=g!=c?g:8*a.length},toX32:function(){for(var j=this.words,m=j.length,o=[],i=0;i<m;i++){var k=j[i];o.push(k.high);o.push(k.low)}return f.create(o,this.sigBytes)},clone:function(){for(var i=h.clone.call(this),j=i.words=this.words.slice(0),k=j.length,e=0;e<k;e++){j[e]=j[e].clone()}return i}})})();(function(){function c(){return h.create.apply(h,arguments)}var f=CryptoJS,b=f.lib.Hasher,i=f.x64,h=i.Word,d=i.WordArray,i=f.algo,k=[c(1116352408,3609767458),c(1899447441,602891725),c(3049323471,3964484399),c(3921009573,2173295548),c(961987163,4081628472),c(1508970993,3053834265),c(2453635748,2937671579),c(2870763221,3664609560),c(3624381080,2734883394),c(310598401,1164996542),c(607225278,1323610764),c(1426881987,3590304994),c(1925078388,4068182383),c(2162078206,991336113),c(2614888103,633803317),c(3248222580,3479774868),c(3835390401,2666613458),c(4022224774,944711139),c(264347078,2341262773),c(604807628,2007800933),c(770255983,1495990901),c(1249150122,1856431235),c(1555081692,3175218132),c(1996064986,2198950837),c(2554220882,3999719339),c(2821834349,766784016),c(2952996808,2566594879),c(3210313671,3203337956),c(3336571891,1034457026),c(3584528711,2466948901),c(113926993,3758326383),c(338241895,168717936),c(666307205,1188179964),c(773529912,1546045734),c(1294757372,1522805485),c(1396182291,2643833823),c(1695183700,2343527390),c(1986661051,1014477480),c(2177026350,1206759142),c(2456956037,344077627),c(2730485921,1290863460),c(2820302411,3158454273),c(3259730800,3505952657),c(3345764771,106217008),c(3516065817,3606008344),c(3600352804,1432725776),c(4094571909,1467031594),c(275423344,851169720),c(430227734,3100823752),c(506948616,1363258195),c(659060556,3750685593),c(883997877,3785050280),c(958139571,3318307427),c(1322822218,3812723403),c(1537002063,2003034995),c(1747873779,3602036899),c(1955562222,1575990012),c(2024104815,1125592928),c(2227730452,2716904306),c(2361852424,442776044),c(2428436474,593698344),c(2756734187,3733110249),c(3204031479,2999351573),c(3329325298,3815920427),c(3391569614,3928383900),c(3515267271,566280711),c(3940187606,3454069534),c(4118630271,4000239992),c(116418474,1914138554),c(174292421,2731055270),c(289380356,3203993006),c(460393269,320620315),c(685471733,587496836),c(852142971,1086792851),c(1017036298,365543100),c(1126000580,2618297676),c(1288033470,3409855158),c(1501505948,4234509866),c(1607167915,987167468),c(1816402316,1246189591)],j=[];(function(){for(var a=0;80>a;a++){j[a]=c()}})();i=i.SHA512=b.extend({_doReset:function(){this._hash=d.create([c(1779033703,4089235720),c(3144134277,2227873595),c(1013904242,4271175723),c(2773480762,1595750129),c(1359893119,2917565137),c(2600822924,725511199),c(528734635,4215389547),c(1541459225,327033209)])},_doProcessBlock:function(a0,aW){for(var aT=this._hash.words,aU=aT[0],aQ=aT[1],aZ=aT[2],aX=aT[3],aY=aT[4],aS=aT[5],aP=aT[6],aT=aT[7],aM=aU.high,aL=aU.low,ab=aQ.high,an=aQ.low,y=aZ.high,am=aZ.low,n=aX.high,al=aX.low,l=aY.high,ak=aY.low,aB=aS.high,aj=aS.low,az=aP.high,ai=aP.low,a1=aT.high,ah=aT.low,aJ=aM,aO=aL,au=ab,aw=an,at=y,av=am,ae=n,ar=al,aI=l,aN=ak,ag=aB,aq=aj,af=az,ap=ai,ad=a1,ao=ah,aH=0;80>aH;aH++){var aE=j[aH];if(16>aH){var aK=aE.high=a0[aW+2*aH]|0,aV=aE.low=a0[aW+2*aH+1]|0}else{var aK=j[aH-15],aV=aK.high,aG=aK.low,aK=(aG<<31|aV>>>1)^(aG<<24|aV>>>8)^aV>>>7,aG=(aV<<31|aG>>>1)^(aV<<24|aG>>>8)^(aV<<25|aG>>>7),ax=j[aH-2],aV=ax.high,aR=ax.low,ax=(aR<<13|aV>>>19)^(aV<<3|aR>>>29)^aV>>>6,aR=(aV<<13|aR>>>19)^(aR<<3|aV>>>29)^(aV<<26|aR>>>6),aV=j[aH-7],ac=aV.high,ay=j[aH-16],aF=ay.high,ay=ay.low,aV=aG+aV.low,aK=aK+ac+(aV>>>0<aG>>>0?1:0),aV=aV+aR,aK=aK+ax+(aV>>>0<aR>>>0?1:0),aV=aV+ay,aK=aK+aF+(aV>>>0<ay>>>0?1:0);aE.high=aK;aE.low=aV}var ac=aI&ag^~aI&af,ay=aN&aq^~aN&ap,aE=aJ&au^aJ&at^au&at,aD=aO&aw^aO&av^aw&av,aG=(aO<<4|aJ>>>28)^(aJ<<30|aO>>>2)^(aJ<<25|aO>>>7),ax=(aJ<<4|aO>>>28)^(aO<<30|aJ>>>2)^(aO<<25|aJ>>>7),aR=k[aH],aA=aR.high,aC=aR.low,aR=ao+((aI<<18|aN>>>14)^(aI<<14|aN>>>18)^(aN<<23|aI>>>9)),aF=ad+((aN<<18|aI>>>14)^(aN<<14|aI>>>18)^(aI<<23|aN>>>9))+(aR>>>0<ao>>>0?1:0),aR=aR+ay,aF=aF+ac+(aR>>>0<ay>>>0?1:0),aR=aR+aC,aF=aF+aA+(aR>>>0<aC>>>0?1:0),aR=aR+aV,aF=aF+aK+(aR>>>0<aV>>>0?1:0),aV=ax+aD,aE=aG+aE+(aV>>>0<ax>>>0?1:0),ad=af,ao=ap,af=ag,ap=aq,ag=aI,aq=aN,aN=ar+aR|0,aI=ae+aF+(aN>>>0<ar>>>0?1:0)|0,ae=at,ar=av,at=au,av=aw,au=aJ,aw=aO,aO=aR+aV|0,aJ=aF+aE+(aO>>>0<aR>>>0?1:0)|0}aL=aU.low=aL+aO|0;aU.high=aM+aJ+(aL>>>0<aO>>>0?1:0)|0;an=aQ.low=an+aw|0;aQ.high=ab+au+(an>>>0<aw>>>0?1:0)|0;am=aZ.low=am+av|0;aZ.high=y+at+(am>>>0<av>>>0?1:0)|0;al=aX.low=al+ar|0;aX.high=n+ae+(al>>>0<ar>>>0?1:0)|0;ak=aY.low=ak+aN|0;aY.high=l+aI+(ak>>>0<aN>>>0?1:0)|0;aj=aS.low=aj+aq|0;aS.high=aB+ag+(aj>>>0<aq>>>0?1:0)|0;ai=aP.low=ai+ap|0;aP.high=az+af+(ai>>>0<ap>>>0?1:0)|0;ah=aT.low=ah+ao|0;aT.high=a1+ad+(ah>>>0<ao>>>0?1:0)|0},_doFinalize:function(){var l=this._data,o=l.words,m=8*this._nDataBytes,n=8*l.sigBytes;o[n>>>5]|=128<<24-n%32;o[(n+128>>>10<<5)+31]=m;l.sigBytes=4*o.length;this._process();this._hash=this._hash.toX32()},blockSize:32});f.SHA512=b._createHelper(i);f.HmacSHA512=b._createHmacHelper(i)})();
        return CryptoJS.SHA512(message);
    },
	
});

Ext.define("Login.modules.LoginForm",{
    extend             : "Login.abstract.Form",
    alias              : "loginform",
    forward            : true,
    initComponent      : function() {
        this.items = this.createLoginFields();
        this.fbar = this.createButtons();
        this.callParent();
    },

    createButtons: function(){
        return [{
            text       : "Login",
            scope      : this,
            handler    : this.login
        },{
            text       : "Create account",
            scope      : this,
            handler    : this.createAccount
        }];
    },

    createLoginFields: function(){
        return [{
            xtype    : "fieldcontainer",
            layout    : "hbox",
            defaultType : "textfield",
            width    : 360,
            items    : [{
                labelAlign    : "top",
                msgTarget     : 'side',
                fieldLabel    : "Email",
                name          : "email",
                allowBlank    : false,
                flex          : 1,
                margins       : {right:3}
            },{
                labelAlign    : "top",
                msgTarget     : 'side',
                inputType     : 'password',
                fieldLabel    : 'Password',
                name          : 'password',
                allowBlank    : false,
                flex          : 1,
                margins       : {left:3},
                listeners     : {
                    scope         : this,
                    specialkey    : function(f,e){
                        if (e.getKey() == e.ENTER) {
                            this.login();
                        }
                    }
                }
            }]
        }];
    },


    login: function(values){
        //Ext.require("Login.Ext.Util.Crypto");
        if(this.getForm().isValid()){
            var values = this.getForm().getValues();
            var Crypto = Ext.create('Login.modules.Crypto');
            var hexPass = Crypto.SHA256(values["password"]).toString();
            values["password"] = hexPass;
            Login.Ajax.request({
                url        : Login.Constants.LOGIN_URL,
                params     : values,
                el         : this.up("window").el,
                scope      : this,
                success    : this.onSuccess,
                failure    : this.onFailure
            });
        }
    },

    onSuccess: function(data){
        if(data.success){
            if(this.forward){
                document.location = Login.Constants.HOME_URL;
            }else{
                var win = this.up("window");
                if(win){
                    win.close();
                }
            }

        }
    },

    onFailure: function(data,response){
        var passwrd = this.down("textfield[name=password]");

        Ext.create("Ext.tip.ToolTip",{
            anchor        : "left",
            target        : passwrd.bodyEl,
            trackMouse    : false,
            html          : data.message,
            autoShow      : true
        });
        passwrd.markInvalid(data.message);
    },

        createAccount: function(){
        if(this.getForm().isValid()){
            var values = this.getForm().getValues();
            Login.Ajax.request({
                url        : Login.Constants.CREATE_ACCOUNT_URL,
                params     : values,
                el         : this.up("window").el,
                scope      : this,
                success    : this.onSuccess,
                failure    : this.onFailure
            });
        }
    }
});