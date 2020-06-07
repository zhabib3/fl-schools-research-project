/* WCM environment init and module loader
 * v 0.1
 */
this.Bb = this.Bb || {};
this.Bb.WCM = this.Bb.WCM || {};


/* Promise-based UI component instance factories */
(function () {
    var self = this;
    /* Loader for UI component */
    var UI = this.UI = this.UI || {};
    [   'Button',
        'EventDetail',
        'Calendar',
        'BaseComponent',
        'ModalContainer',
        'ModalDialog',
        'DatePicker',
        'Combobox'
    ].forEach(function (item) {
        UI[item] = function () {
            var args = Array.prototype.slice.call(arguments);
            args.unshift(null);
            return new self.RSVP.Promise(function (resolve, reject) {
                self.use(['UI.' + item], function (module)
                {
                    var component = new (Function.prototype.bind.apply(module, args));

                    if (typeof (component.selfResolve) != "undefined" || component.selfResolve)
                    {
                        component.resolve = resolve;
                        component.reject = reject;
                    }
                    else
                    {
                        resolve(component);
                    }
                }, reject);
            });
        };
    });
}).call(this.Bb.WCM);


/* rsvp.min.js pre-loaded into Bb.WCM.RSVP */
(function () {
    (function (t, e) { "object" == typeof exports && "undefined" != typeof module ? e(exports) : "function" == typeof define && define.amd ? define(["exports"], e) : e(t.RSVP = t.RSVP || {}) })(this, function (t) { "use strict"; function e(t, e) { for (var r = 0, n = t.length; r < n; r++) if (t[r] === e) return r; return -1 } function r(t) { var e = t._promiseCallbacks; e || (e = t._promiseCallbacks = {}); return e } function n(t, e) { if (2 !== arguments.length) return jt[t]; jt[t] = e } function o(t) { var e = typeof t; return null !== t && ("object" === e || "function" === e) } function i(t) { return "function" == typeof t } function u(t) { return null !== t && "object" == typeof t } function a(t) { return null !== t && "object" == typeof t } function s() { setTimeout(function () { for (var t = 0; t < St.length; t++) { var e = St[t], r = e.payload; r.guid = r.key + r.id; r.childGuid = r.key + r.childId; r.error && (r.stack = r.error.stack); jt.trigger(e.name, e.payload) } St.length = 0 }, 50) } function c(t, e, r) { 1 === St.push({ name: t, payload: { key: e._guidKey, id: e._id, eventName: t, detail: e._result, childId: r && r._id, label: e._label, timeStamp: Ot(), error: jt["instrument-with-stack"] ? new Error(e._label) : null } }) && s() } function f(t, e) { var r = this; if (t && "object" == typeof t && t.constructor === r) return t; var n = new r(h, e); m(n, t); return n } function l() { return new TypeError("A promises callback cannot return that same promise.") } function h() { } function p(t) { try { return t.then } catch (e) { kt.error = e; return kt } } function y(t, e, r, n) { try { t.call(e, r, n) } catch (o) { return o } } function v(t, e, r) { jt.async(function (t) { var n = !1, o = y(r, e, function (r) { if (!n) { n = !0; e !== r ? m(t, r, void 0) : b(t, r) } }, function (e) { if (!n) { n = !0; g(t, e) } }, "Settle: " + (t._label || " unknown promise")); if (!n && o) { n = !0; g(t, o) } }, t) } function d(t, e) { if (e._state === Pt) b(t, e._result); else if (e._state === Rt) { e._onError = null; g(t, e._result) } else j(e, void 0, function (r) { e !== r ? m(t, r, void 0) : b(t, r) }, function (e) { return g(t, e) }) } function _(t, e, r) { var n = e.constructor === t.constructor && r === P && t.constructor.resolve === f; if (n) d(t, e); else if (r === kt) { g(t, kt.error); kt.error = null } else i(r) ? v(t, e, r) : b(t, e) } function m(t, e) { t === e ? b(t, e) : o(e) ? _(t, e, p(e)) : b(t, e) } function w(t) { t._onError && t._onError(t._result); E(t) } function b(t, e) { if (t._state === At) { t._result = e; t._state = Pt; 0 === t._subscribers.length ? jt.instrument && c("fulfilled", t) : jt.async(E, t) } } function g(t, e) { if (t._state === At) { t._state = Rt; t._result = e; jt.async(w, t) } } function j(t, e, r, n) { var o = t._subscribers, i = o.length; t._onError = null; o[i] = e; o[i + Pt] = r; o[i + Rt] = n; 0 === i && t._state && jt.async(E, t) } function E(t) { var e = t._subscribers, r = t._state; jt.instrument && c(r === Pt ? "fulfilled" : "rejected", t); if (0 !== e.length) { for (var n = void 0, o = void 0, i = t._result, u = 0; u < e.length; u += 3) { n = e[u]; o = e[u + r]; n ? S(r, n, o, i) : o(i) } t._subscribers.length = 0 } } function T() { this.error = null } function O(t, e) { try { return t(e) } catch (r) { xt.error = r; return xt } } function S(t, e, r, n) { var o = i(r), u = void 0, a = void 0; if (o) { u = O(r, n); if (u === xt) { a = u.error; u.error = null } else if (u === e) { g(e, l()); return } } else u = n; e._state !== At || (o && void 0 === a ? m(e, u) : void 0 !== a ? g(e, a) : t === Pt ? b(e, u) : t === Rt && g(e, u)) } function A(t, e) { var r = !1; try { e(function (e) { if (!r) { r = !0; m(t, e) } }, function (e) { if (!r) { r = !0; g(t, e) } }) } catch (n) { g(t, n) } } function P(t, e, r) { var n = this, o = n._state; if (o === Pt && !t || o === Rt && !e) { jt.instrument && c("chained", n, n); return n } n._onError = null; var i = new n.constructor(h, r), u = n._result; jt.instrument && c("chained", n, i); if (o === At) j(n, i, t, e); else { var a = o === Pt ? t : e; jt.async(function () { return S(o, i, a, u) }) } return i } function R(t, e, r) { return t === Pt ? { state: "fulfilled", value: r } : { state: "rejected", reason: r } } function k(t, e) { return Tt(t) ? new Mt(this, t, (!0), e).promise : this.reject(new TypeError("Promise.all must be called with an array"), e) } function x(t, e) { var r = this, n = new r(h, e); if (!Tt(t)) { g(n, new TypeError("Promise.race must be called with an array")); return n } for (var o = 0; n._state === At && o < t.length; o++) j(r.resolve(t[o]), void 0, function (t) { return m(n, t) }, function (t) { return g(n, t) }); return n } function M(t, e) { var r = this, n = new r(h, e); g(n, t); return n } function C() { throw new TypeError("You must pass a resolver function as the first argument to the promise constructor") } function I() { throw new TypeError("Failed to construct 'Promise': Please use the 'new' operator, this object constructor cannot be called as a function.") } function N() { this.value = void 0 } function V(t) { try { return t.then } catch (e) { Vt.value = e; return Vt } } function D(t, e, r) { try { t.apply(e, r) } catch (n) { Vt.value = n; return Vt } } function K(t, e) { for (var r = {}, n = t.length, o = new Array(n), i = 0; i < n; i++) o[i] = t[i]; for (var u = 0; u < e.length; u++) { var a = e[u]; r[a] = o[u + 1] } return r } function U(t) { for (var e = t.length, r = new Array(e - 1), n = 1; n < e; n++) r[n - 1] = t[n]; return r } function q(t, e) { return { then: function (r, n) { return t.call(e, r, n) } } } function F(t, e) { var r = function () { for (var r = this, n = arguments.length, o = new Array(n + 1), i = !1, u = 0; u < n; ++u) { var a = arguments[u]; if (!i) { i = W(a); if (i === Dt) { var s = new Nt(h); g(s, Dt.value); return s } i && i !== !0 && (a = q(i, a)) } o[u] = a } var c = new Nt(h); o[n] = function (t, r) { t ? g(c, t) : void 0 === e ? m(c, r) : e === !0 ? m(c, U(arguments)) : Tt(e) ? m(c, K(arguments, e)) : m(c, r) }; return i ? L(c, o, t, r) : G(c, o, t, r) }; r.__proto__ = t; return r } function G(t, e, r, n) { var o = D(r, n, e); o === Vt && g(t, o.value); return t } function L(t, e, r, n) { return Nt.all(e).then(function (e) { var o = D(r, n, e); o === Vt && g(t, o.value); return t }) } function W(t) { return !(!t || "object" != typeof t) && (t.constructor === Nt || V(t)) } function Y(t, e) { return Nt.all(t, e) } function $(t, e) { if (!t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); return !e || "object" != typeof e && "function" != typeof e ? t : e } function z(t, e) { if ("function" != typeof e && null !== e) throw new TypeError("Super expression must either be null or a function, not " + typeof e); t.prototype = Object.create(e && e.prototype, { constructor: { value: t, enumerable: !1, writable: !0, configurable: !0 } }); e && (Object.setPrototypeOf ? Object.setPrototypeOf(t, e) : t.__proto__ = e) } function B(t, e) { return Tt(t) ? new Kt(Nt, t, e).promise : Nt.reject(new TypeError("Promise.allSettled must be called with an array"), e) } function H(t, e) { return Nt.race(t, e) } function J(t, e) { if (!t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); return !e || "object" != typeof e && "function" != typeof e ? t : e } function Q(t, e) { if ("function" != typeof e && null !== e) throw new TypeError("Super expression must either be null or a function, not " + typeof e); t.prototype = Object.create(e && e.prototype, { constructor: { value: t, enumerable: !1, writable: !0, configurable: !0 } }); e && (Object.setPrototypeOf ? Object.setPrototypeOf(t, e) : t.__proto__ = e) } function X(t, e) { return u(t) ? new qt(Nt, t, e).promise : Nt.reject(new TypeError("Promise.hash must be called with an object"), e) } function Z(t, e) { if (!t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); return !e || "object" != typeof e && "function" != typeof e ? t : e } function tt(t, e) { if ("function" != typeof e && null !== e) throw new TypeError("Super expression must either be null or a function, not " + typeof e); t.prototype = Object.create(e && e.prototype, { constructor: { value: t, enumerable: !1, writable: !0, configurable: !0 } }); e && (Object.setPrototypeOf ? Object.setPrototypeOf(t, e) : t.__proto__ = e) } function et(t, e) { return u(t) ? new Ft(Nt, t, (!1), e).promise : Nt.reject(new TypeError("RSVP.hashSettled must be called with an object"), e) } function rt(t) { setTimeout(function () { throw t }); throw t } function nt(t) { var e = { resolve: void 0, reject: void 0 }; e.promise = new Nt(function (t, r) { e.resolve = t; e.reject = r }, t); return e } function ot(t, e, r) { return Tt(t) ? i(e) ? Nt.all(t, r).then(function (t) { for (var n = t.length, o = new Array(n), i = 0; i < n; i++) o[i] = e(t[i]); return Nt.all(o, r) }) : Nt.reject(new TypeError("RSVP.map expects a function as a second argument"), r) : Nt.reject(new TypeError("RSVP.map must be called with an array"), r) } function it(t, e) { return Nt.resolve(t, e) } function ut(t, e) { return Nt.reject(t, e) } function at(t, e) { return Nt.all(t, e) } function st(t, e) { return Nt.resolve(t, e).then(function (t) { return at(t, e) }) } function ct(t, e, r) { if (!(Tt(t) || u(t) && void 0 !== t.then)) return Nt.reject(new TypeError("RSVP.filter must be called with an array or promise"), r); if (!i(e)) return Nt.reject(new TypeError("RSVP.filter expects function as a second argument"), r); var n = Tt(t) ? at(t, r) : st(t, r); return n.then(function (t) { for (var n = t.length, o = new Array(n), i = 0; i < n; i++) o[i] = e(t[i]); return at(o, r).then(function (e) { for (var r = new Array(n), o = 0, i = 0; i < n; i++) if (e[i]) { r[o] = t[i]; o++ } r.length = o; return r }) }) } function ft(t, e) { Ht[Gt] = t; Ht[Gt + 1] = e; Gt += 2; 2 === Gt && Jt() } function lt() { var t = process.nextTick, e = process.versions.node.match(/^(?:(\d+)\.)?(?:(\d+)\.)?(\*|\d+)$/); Array.isArray(e) && "0" === e[1] && "10" === e[2] && (t = setImmediate); return function () { return t(dt) } } function ht() { return "undefined" != typeof Lt ? function () { Lt(dt) } : vt() } function pt() { var t = 0, e = new $t(dt), r = document.createTextNode(""); e.observe(r, { characterData: !0 }); return function () { return r.data = t = ++t % 2 } } function yt() { var t = new MessageChannel; t.port1.onmessage = dt; return function () { return t.port2.postMessage(0) } } function vt() { return function () { return setTimeout(dt, 1) } } function dt() { for (var t = 0; t < Gt; t += 2) { var e = Ht[t], r = Ht[t + 1]; e(r); Ht[t] = void 0; Ht[t + 1] = void 0 } Gt = 0 } function _t() { try { var t = require, e = t("vertx"); Lt = e.runOnLoop || e.runOnContext; return ht() } catch (r) { return vt() } } function mt(t, e, r) { e in t ? Object.defineProperty(t, e, { value: r, enumerable: !0, configurable: !0, writable: !0 }) : t[e] = r; return t } function wt() { jt.on.apply(jt, arguments) } function bt() { jt.off.apply(jt, arguments) } var gt = { mixin: function (t) { t.on = this.on; t.off = this.off; t.trigger = this.trigger; t._promiseCallbacks = void 0; return t }, on: function (t, n) { if ("function" != typeof n) throw new TypeError("Callback must be a function"); var o = r(this), i = void 0; i = o[t]; i || (i = o[t] = []); e(i, n) === -1 && i.push(n) }, off: function (t, n) { var o = r(this), i = void 0, u = void 0; if (n) { i = o[t]; u = e(i, n); u !== -1 && i.splice(u, 1) } else o[t] = [] }, trigger: function (t, e, n) { var o = r(this), i = void 0, u = void 0; if (i = o[t]) for (var a = 0; a < i.length; a++) { u = i[a]; u(e, n) } } }, jt = { instrument: !1 }; gt.mixin(jt); var Et = void 0; Et = Array.isArray ? Array.isArray : function (t) { return "[object Array]" === Object.prototype.toString.call(t) }; var Tt = Et, Ot = Date.now || function () { return (new Date).getTime() }, St = [], At = void 0, Pt = 1, Rt = 2, kt = new T, xt = new T, Mt = function () { function t(t, e, r, n) { this._instanceConstructor = t; this.promise = new t(h, n); this._abortOnReject = r; this._init.apply(this, arguments) } t.prototype._init = function (t, e) { var r = e.length || 0; this.length = r; this._remaining = r; this._result = new Array(r); this._enumerate(e); 0 === this._remaining && b(this.promise, this._result) }; t.prototype._enumerate = function (t) { for (var e = this.length, r = this.promise, n = 0; r._state === At && n < e; n++) this._eachEntry(t[n], n) }; t.prototype._settleMaybeThenable = function (t, e) { var r = this._instanceConstructor, n = r.resolve; if (n === f) { var o = p(t); if (o === P && t._state !== At) { t._onError = null; this._settledAt(t._state, e, t._result) } else if ("function" != typeof o) { this._remaining--; this._result[e] = this._makeResult(Pt, e, t) } else if (r === Nt) { var i = new r(h); _(i, t, o); this._willSettleAt(i, e) } else this._willSettleAt(new r(function (e) { return e(t) }), e) } else this._willSettleAt(n(t), e) }; t.prototype._eachEntry = function (t, e) { if (a(t)) this._settleMaybeThenable(t, e); else { this._remaining--; this._result[e] = this._makeResult(Pt, e, t) } }; t.prototype._settledAt = function (t, e, r) { var n = this.promise; if (n._state === At) if (this._abortOnReject && t === Rt) g(n, r); else { this._remaining--; this._result[e] = this._makeResult(t, e, r); 0 === this._remaining && b(n, this._result) } }; t.prototype._makeResult = function (t, e, r) { return r }; t.prototype._willSettleAt = function (t, e) { var r = this; j(t, void 0, function (t) { return r._settledAt(Pt, e, t) }, function (t) { return r._settledAt(Rt, e, t) }) }; return t }(), Ct = "rsvp_" + Ot() + "-", It = 0, Nt = function () { function t(e, r) { this._id = It++; this._label = r; this._state = void 0; this._result = void 0; this._subscribers = []; jt.instrument && c("created", this); if (h !== e) { "function" != typeof e && C(); this instanceof t ? A(this, e) : I() } } t.prototype._onError = function (t) { var e = this; jt.after(function () { e._onError && jt.trigger("error", t, e._label) }) }; t.prototype["catch"] = function (t, e) { return this.then(void 0, t, e) }; t.prototype["finally"] = function (t, e) { var r = this, n = r.constructor; return r.then(function (e) { return n.resolve(t()).then(function () { return e }) }, function (e) { return n.resolve(t()).then(function () { throw e }) }, e) }; return t }(); Nt.cast = f; Nt.all = k; Nt.race = x; Nt.resolve = f; Nt.reject = M; Nt.prototype._guidKey = Ct; Nt.prototype.then = P; var Vt = new N, Dt = new N, Kt = function (t) { function e(e, r, n) { return $(this, t.call(this, e, r, !1, n)) } z(e, t); return e }(Mt); Kt.prototype._makeResult = R; var Ut = Object.prototype.hasOwnProperty, qt = function (t) { function e(e, r) { var n = !(arguments.length > 2 && void 0 !== arguments[2]) || arguments[2], o = arguments[3]; return J(this, t.call(this, e, r, n, o)) } Q(e, t); e.prototype._init = function (t, e) { this._result = {}; this._enumerate(e); 0 === this._remaining && b(this.promise, this._result) }; e.prototype._enumerate = function (t) { var e = this, r = e.promise, n = []; for (var o in t) r._state === At && Ut.call(t, o) && n.push({ position: o, entry: t[o] }); var i = n.length; e._remaining = i; for (var u = void 0, a = 0; r._state === At && a < i; a++) { u = n[a]; e._eachEntry(u.entry, u.position) } }; return e }(Mt), Ft = function (t) { function e(e, r, n) { return Z(this, t.call(this, e, r, !1, n)) } tt(e, t); return e }(qt); Ft.prototype._makeResult = R; var Gt = 0, Lt = void 0, Wt = "undefined" != typeof window ? window : void 0, Yt = Wt || {}, $t = Yt.MutationObserver || Yt.WebKitMutationObserver, zt = "undefined" == typeof self && "undefined" != typeof process && "[object process]" === {}.toString.call(process), Bt = "undefined" != typeof Uint8ClampedArray && "undefined" != typeof importScripts && "undefined" != typeof MessageChannel, Ht = new Array(1e3), Jt = void 0; Jt = zt ? lt() : $t ? pt() : Bt ? yt() : void 0 === Wt && "function" == typeof require ? _t() : vt(); var Qt = void 0; if ("object" == typeof self) Qt = self; else { if ("object" != typeof global) throw new Error("no global: `self` or `global` found"); Qt = global } var Xt; jt.async = ft; jt.after = function (t) { return setTimeout(t, 0) }; var Zt = it, te = function (t, e) { return jt.async(t, e) }; if ("undefined" != typeof window && "object" == typeof window.__PROMISE_INSTRUMENTATION__) { var ee = window.__PROMISE_INSTRUMENTATION__; n("instrument", !0); for (var re in ee) ee.hasOwnProperty(re) && wt(re, ee[re]) } var ne = (Xt = { asap: ft, cast: Zt, Promise: Nt, EventTarget: gt, all: Y, allSettled: B, race: H, hash: X, hashSettled: et, rethrow: rt, defer: nt, denodeify: F, configure: n, on: wt, off: bt, resolve: it, reject: ut, map: ot }, mt(Xt, "async", te), mt(Xt, "filter", ct), Xt); t["default"] = ne; t.asap = ft; t.cast = Zt; t.Promise = Nt; t.EventTarget = gt; t.all = Y; t.allSettled = B; t.race = H; t.hash = X; t.hashSettled = et; t.rethrow = rt; t.defer = nt; t.denodeify = F; t.configure = n; t.on = wt; t.off = bt; t.resolve = it; t.reject = ut; t.map = ot; t.async = te; t.filter = ct; Object.defineProperty(t, "__esModule", { value: !0 }) });
}).call(this.Bb.WCM);

/* module loader */
(function () {
    var root = this;
    var base = (document.currentScript || document.scripts[document.scripts.length - 1]).src.replace('WCM.js', '');
    var deps = {
        loaded: {
            'RSVP': root.RSVP,
            'use': function (module) { return deps.loaded[module] || null; },
            'exports': root
        },
        queue: [],
        waiting: [],
        failed: []
    };

    /* private: map module name to partial path */
    function mapModuleName(module) {
        return module
            .replace(/^UI\.(?:[^.]+\.)*(.*)$/, '$&/$1')     /* map UI component modules to respective subfolders */
            .replace(/\./g, '/');                             /* map namespaces to folders */
    }

    /* private: do extra stuff before a module starts loading */
    function beforeScriptLoad(module) {
        var styleLibs = ["lib.flatpickr"];

        if (module.indexOf('UI.') === 0 || styleLibs.indexOf(module) !== -1) {
            /* load CSS for the UI component */
            var css = document.createElement('link');
            css.rel = 'Stylesheet';
            css.type = 'text/css';
            css.setAttribute('data-wcm-module', module);
            css.href = base + mapModuleName(module) + '.css';
            (document.getElementsByTagName('head')[0]).appendChild(css);
        }
    }

    /* private: do extra stuff after a module is fully loaded */
    function afterScriptLoad(module) {
    }

    /* private: map module name to module reference (or instance, if needed) */
    function mapModuleInstance(module) {
        return root.getModule(module);
    }

    /* private: test if module has unsatisfied dependencies */
    function unmetDeps(requires) {
        return requires.filter(function (req) { return !deps.loaded[req]; });
    }

    /* private: test if variable contains a function */
    function isFunction(o) {
        return Object.prototype.toString.call(o) === '[object Function]';
    }

    /* private: test if variable contains an array */
    function isArray(o) {
        return Object.prototype.toString.call(o) === '[object Array]';
    }

    /* private: register module or run anonymous use function when all dependencies satisfied */
    function attachModule(name, value, requires) {
        if (isFunction(value)) { /* run factory function */
            var args = [];
            requires.forEach(function (req) { args.push(mapModuleInstance(req)); });
            value = value.apply(this, args);
        }
        if (name !== null) {    /* register module */
            if (typeof (value) === "undefined")
                throw "WCM loader error: module " + name + " returned undefined!"

            deps.loaded[name] = deps.loaded[name] || value;
            deps.queue = deps.queue.filter(function (req) { return req !== name; });

            var pointer = root;            /* append module to the Bb.WCM structure */
            var path = name.split('.');
            var holder = path.pop();
            path.forEach(function (p) {
                pointer[p] = pointer[p] || {};
                pointer = pointer[p];
            });
            pointer[holder] = pointer[holder] || deps.loaded[name];
        }
    };

    /* private: returns 'true' if module is ajax loaded otherwise returns 'false' */
    function isAjaxLoaded(modulename) {
        prefix = "lib.";
        return modulename.indexOf(prefix) == 0;
    }

    /* private: process modules with newly satisfied dependencies */
    function processWaiting() {
        do {
            var ready = [], waiting = [];
            deps.waiting.forEach(function (w) { (unmetDeps(w.req).length ? waiting : ready).push(w); });
            deps.waiting = waiting;
            ready.forEach(function (r) { attachModule(r.name, r.fn, r.req); });
        } while (ready.length);
    }

    /* private: script cleanup */
    function scriptFinished(evt) {
        var script = evt.currentTarget || evt.srcElement;
        removeEventListener(script, onLoad, 'load');
        removeEventListener(script, onError, 'error');
        return script.getAttribute('data-wcm-module');
    }

    /* private: script loaded */
    function onLoad(param) {
        if (typeof (param) != 'string') {
            if (param.type !== 'load')
                return;

            var module = scriptFinished(param);
        }
        else {
            var module = param;
        }

        if (!deps.waiting.filter(function (w) { return w.name === module; }).length) {
            /* only mark self as loaded if no requirements pending */
            deps.loaded[module] = deps.loaded[module] || true;
            deps.queue = deps.queue.filter(function (req) { return req !== module; });
        }
        afterScriptLoad(module);
        processWaiting();
    }

    /* private: script not found */
    function onError(param) {
        if (typeof (param) == 'string') {
            //console.log('WCM: failed to load module "' + param + '"');
        }
        else {
            var module = scriptFinished(param);
            //console.log('WCM: failed to load module "' + module + '"');
            dequeueFailed(module);
        }
    }

    /* private: clean up failed dependencies */
    function dequeueFailed(module) {
        deps.queue = deps.queue.filter(function (req) { return req !== module; });
        deps.failed.push(module);
        var failed = [], waiting = [];
        deps.waiting.forEach(function (w) { (w.req.indexOf(module) === -1 ? waiting : failed).push(w); });
        deps.waiting = waiting;
        failed.forEach(function (r) {
            if (r.name !== null) {
                //console.log('WCM: unsatisfied dependency "' + module + '" in module "' + r.name + '"');
                dequeueFailed(r.name);
            }
            else {
                //console.log('WCM: unsatisfied dependency "' + module + '" in use block: ');
                //console.log(r.fn);
            }
            if (r.err) {
                r.err({ status: 'error', description: 'Failed to load module', module: module });
            }
        });
    }

    /* private: start loading a module script */
    function loadScript(module) {
        if (deps.queue.indexOf(module) === -1 && deps.failed.indexOf(module) === -1) {
            deps.queue.push(module);
            beforeScriptLoad(module);

            if (isAjaxLoaded(module)) {
                var loader = new XMLHttpRequest();
                loader.open('GET', base + mapModuleName(module) + '.js', true);
                var self = this;

                loader.onreadystatechange = function () {
                    if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
                        new Function(' function define(a, b) { Bb.WCM.module(\"' + module + '\", a, b);  }; define.amd=true;' + loader.responseText + "\n//# sourceURL=/" + module + '.js').bind(self)();
                        onLoad(module);
                    }
                    else if (this.readyState == XMLHttpRequest.DONE) {
                        onError(module);
                    }
                };

                loader.send();
            }
            else {
                var script = document.createElement('script');
                script.type = 'text/javascript';
                script.charset = 'utf-8';
                script.async = true;
                script.setAttribute('data-wcm-module', module);
                script.addEventListener('load', onLoad, false);
                script.addEventListener('error', onError, false);
                script.src = base + mapModuleName(module) + '.js';
                (document.getElementsByTagName('head')[0]).appendChild(script);
            }
        }
    };

    /* public: inheritance  */
    this.extend = function (child, parent) {
        var tempConstructor = function () { };
        tempConstructor.prototype = parent.prototype;

        child.prototype = new tempConstructor();
        child._superClass = parent.prototype;

        child.prototype.constructor = child;
    };

    /* public: checks params  */
    this.checkParams = function(params, defparams)
    {
        params = params || [];
        for (var key in params) {
            var isDefined = false;

            for (var i = 0; i < defparams.length; ++i) {
                if (defparams[i]["name"] == key) {
                    defparams[i]["seen"] = true;
                    isDefined = true;
                    break;
                }
            }

            if (!isDefined)
                throw "The parameter '" + key + "' is unknown.";
        }

        for (var i = 0; i < defparams.length; ++i) {
            if (typeof (defparams[i]["seen"]) == "undefined") {
                if (defparams[i]["mandatory"] === true) {
                    throw "The parameter '" + defparams[i]["name"] + "' is missing.";
                }
                else {
                    if (typeof (defparams[i]["default"]) != "undefined")
                        params[defparams[i]["name"]] = defparams[i]["default"];
                }
            }
        }

        return params;
    }

    /* public: register a module */
    this.module = (function (name, requires, fn, error) {
        if (!fn) {
            fn = requires;
            requires = [];
            if (isFunction(fn)) {
                requires.push('use');
                fn.toString()                // parse source to get required modules
                    .replace(/\/\*[\s\S]*?\*\/|([^:"'=]|^)\/\/.*$/mg, function (match, p) { return p || ''; })
                    .replace(/[^.]\s*use\s*\(\s*["']([^'"\s]+)["']\s*\)/g, function (match, d) { requires.push(d); });
            }
            else {
                if (name !== null) {
                    attachModule(name, fn, []);
                }
                return;
            }
        }

        var unsat = unmetDeps(requires);
        if (!unsat.length) {
            attachModule(name, fn, requires);
        }
        else {
            deps.waiting.push({ fn: fn, name: name, req: requires, err: error });
            unsat.forEach(loadScript);
        }
    }).bind(this);


    /* public: run an anonymous function with dependencies */
    this.use = (function (requires, fn, error) {
        if (!fn && isArray(requires)) {
            var ns = this;
            return new this.RSVP.Promise(function (resolve, reject) {
                ns.module(null, requires, resolve, reject);
            });
        }
        this.module(null, requires, fn, error);
    }).bind(this);


    /* public: get a loaded module by name, or null if module not loaded */
    this.getModule = function (module) {
        return deps.loaded[module] || null;
    }

}).call(this.Bb.WCM);
