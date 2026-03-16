# Migration Report: script\Automatic.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Automatic.lua
+++ patched/script\Automatic.lua
@@ -1,50 +1,76 @@
--- VERSION 3.16
--- I ask that you please do not rename Automatic.lua - Thankyou
-
---#region Documentation
-
----Documentation Assumes that TDTD's library is in the environemnt
-
---#endregion
---#region Shortcuts
-
-AutoFlatSprite = LoadSprite('ui/menu/white_32.png')
-AutoColors = {
-	background_dark = { 0.28627450980392, 0.25490196078431, 0.38039215686275, 1 },
-	background_light = { 0.41960784313725, 0.39607843137255, 0.58823529411765, 1 },
-	wood_dark = { 0.6, 0.33725490196078, 0.42352941176471, 1 },
-	wood_light = { 0.78039215686275, 0.53333333333333, 0.56470588235294, 1 },
-	rock_dark = { 0.41960784313725, 0.38039215686275, 0.46666666666667, 1 },
-	rock_light = { 0.49803921568627, 0.46274509803922, 0.55686274509804, 1 },
-	green_dark = { 0.3843137254902, 0.76078431372549, 0.76078431372549, 1 },
-	green_light = { 0.4156862745098, 0.90980392156863, 0.63529411764706, 1 },
-	jade_dark = { 0.33725490196078, 0.52156862745098, 0.6, 1 },
-	jade_light = { 0.29411764705882, 0.68627450980392, 0.69019607843137, 1 },
-	aqua_dark = { 0.28627450980392, 0.46666666666667, 0.58039215686275, 1 },
-	aqua_light = { 0.32156862745098, 0.60392156862745, 0.78039215686275, 1 },
-	pastel_dark = { 1, 0.7921568627451, 0.83137254901961, 1 },
-	pastel_light = { 0.80392156862745, 0.70588235294118, 0.85882352941176, 1 },
-	pink_dark = { 0.70196078431373, 0.45098039215686, 0.64313725490196, 1 },
-	pink_light = { 0.94901960784314, 0.57647058823529, 0.86274509803922, 1 },
-	purple_dark = { 0.56470588235294, 0.34117647058824, 0.63921568627451, 1 },
-	purple_light = { 0.77647058823529, 0.45098039215686, 0.8156862745098, 1 },
-	yellow_dark = { 0.7921568627451, 0.65490196078431, 0.32156862745098, 1 },
-	yellow_light = { 0.89803921568627, 0.75686274509804, 0.36862745098039, 1 },
-	amber_dark = { 0.7843137254902, 0.50196078431373, 0.28627450980392, 1 },
-	amber_light = { 0.96470588235294, 0.63921568627451, 0.18039215686275, 1 },
-	red_dark = { 0.72549019607843, 0.35686274509804, 0.48627450980392, 1 },
-	red_light = { 0.84313725490196, 0.33333333333333, 0.41960784313725, 1 },
-	white_dark = { 0.84705882352941, 0.74509803921569, 0.61960784313725, 1 },
-	white_light = { 0.96470588235294, 0.91372549019608, 0.80392156862745, 1 },
-	blue_dark = { 0.2078431372549, 0.31372549019608, 0.43921568627451, 1 },
-	blue_light = { 0.19607843137255, 0.61176470588235, 0.78823529411765, 1 },
-	alert_dark = { 0.22352941176471, 0.098039215686275, 0.2, 1 },
-	alert_light = { 0.74901960784314, 0.21960784313725, 0.49019607843137, 1 },
+#version 2
+local RegistryTableMeta = {
+	__index = function(self, key)
+		key = key:lower()
+		local path = AutoKey(rawget(self, '__path'), key)
+		if not HasKey(path) then
+			return nil
+		end
+		
+		local type = GetString(AutoKey(path, '__type'))
+		
+		if type == 'table' then
+			return AutoRegistryBindedTable(path)
+		else
+			local str = GetString(path)
+			
+			if type == 'number' then
+				return tonumber(str)
+			end
+			
+			return str
+		end
+	end,
+	__newindex = function(self, key, value)
+		key = key:lower()
+		local path = AutoKey(rawget(self, '__path'), key)
+		
+		local function dive(p, v)
+			if type(v) ~= "table" then
+				SetString(p, v, true)
+				
+				if type(v) ~= "nil" then
+					SetString(AutoKey(p, '__type'), type(v), true)
+				end
+			else
+				SetString(AutoKey(p, '__type'), 'table', true)
+				for k, set in pairs(v) do
+					dive(AutoKey(p, k), set)
+				end
+			end
+		end
+		
+		dive(path, value)
+	end,
+	__call = function(self)
+		local path = rawget(self, '__path')
+		
+		local function dive(p)
+			local keys = ListKeys(p)
+			local full = {}
+			
+			for i = 1, #keys do
+				local child = AutoKey(p, keys[i])
+				
+				if keys[i] ~= '__type' then
+					local t = GetString(AutoKey(child, '__type'))
+					if t == 'table' then
+						full[keys[i]] = dive(child)
+					else
+						local str = GetString(child)
+						local num = tonumber(str)
+						full[keys[i]] = num or str
+					end
+				end
+			end
+			
+			return full
+		end
+		
+		return dive(path)
+	end
 }
 
----Creates pitch frequencies for UiSound
----@param baseline string
----@return { C:number, Cs:number, D:number, Ds:number, E:number, F:number, Fs:number, G:number, Gs:number, A:number, As:number, B:number }
 function AutoNoteFrequency(baseline)
 	local f = {
 		C  = 261.63,
@@ -69,28 +95,11 @@
 	return tuned
 end
 
---#endregion
---#region Arithmetic
-
----Sigmoid function, Can be used for juicy UI and smooth easing among other things.
----
----https://www.desmos.com/calculator/cmmwrjtyit?invertedColors
----@param v number? Input number, if nil then it will be a Random number between 0 and 1
----@param max number The Maximum value
----@param steep number How steep the curve is
----@param offset number The horizontal offset of the middle of the curve
----@return number
 function AutoSigmoid(v, max, steep, offset)
 	v = AutoDefault(v, math.random(0, 10000) / 10000)
 	return (max or 1) / (1 + math.exp((v - (offset or 0.5)) * (steep or -10)))
 end
 
----Rounds a number.
----
----This was a Challenge by @TallTim and @1ssnl to make the smallest rounding function, but I expanded it to make it easier to read and a little more efficent
----@param v number Input number
----@param increment number? The lowest increment. A Step of 1 will round the number to 1, A step of 5 will round it to the closest increment of 5, A step of 0.1 will round to the tenth. Default is 1
----@return number
 function AutoRound(v, increment)
 	increment = AutoDefault(increment, 1)
 	if increment == 0 then return v end
@@ -98,14 +107,6 @@
 	return math.floor(v * s + 0.5) / s
 end
 
----Maps a value from range a1-a2 to range b1-b2
----@param v number Input number
----@param a1 number Goes from the range of number a1
----@param a2 number To number a2
----@param b1 number To the range of b1
----@param b2 number To number b2
----@param clamp boolean? Clamp the number between b1 and b2, Default is false
----@return number
 function AutoMap(v, a1, a2, b1, b2, clamp)
 	clamp = AutoDefault(clamp, false)
 	if a1 == a2 then return b2 end
@@ -113,21 +114,12 @@
 	return clamp and AutoClamp(mapped, math.min(b1, b2), math.max(b1, b2)) or mapped
 end
 
----Limits a value from going below the min and above the max
----@param v number The number to clamp
----@param min number? The minimum the number can be, Default is 0
----@param max number? The maximum the number can be, Default is 1
----@return number
 function AutoClamp(v, min, max)
 	min = AutoDefault(min, 0)
 	max = AutoDefault(max, 1)
 	return math.max(math.min(v, max), min)
 end
 
----Limits a value from going below the min and above the max
----@param v number The number to clamp
----@param max number? The maximum the length of the number can be, Default is 1
----@return number
 function AutoClampLength(v, max)
 	max = AutoDefault(max, 1)
 	if v < -max then
@@ -139,11 +131,6 @@
 	end
 end
 
----Wraps a value inbetween a range, Thank you iaobardar for the Optimization
----@param v number The number to wrap
----@param min number? The minimum range
----@param max number? The maximum range
----@return number
 function AutoWrap(v, min, max)
 	min = AutoDefault(min, 0)
 	max = AutoDefault(max, 1)
@@ -151,25 +138,10 @@
 	return (v - min) % ((max + 1) - min) + min
 end
 
----Linerarly Iterpolates between `a` and `b` by fraction `t`
----
----Does not clamp
----@param a number Goes from number A
----@param b number To number B
----@param t number Interpolated by T
----@return number
 function AutoLerp(a, b, t)
 	return (1 - t) * a + t * b
 end
 
----Spherically Iterpolates between `a` and `b` by fraction `t`.
----
----Basically Lerp but with wrapping
----@param a number Goes from number A
----@param b number To number B
----@param t number Interpolated by T
----@param w number Wraps at
----@return number
 function AutoLerpWrap(a, b, t, w)
 	local m = w
 	local da = (b - a) % m
@@ -177,13 +149,6 @@
 	return a + n * t
 end
 
----Moves `a` towards `b` by amount `t`
----
----Will clamp as to not overshoot
----@param a number Goes from number A
----@param b number To number B
----@param t number Moved by T
----@return number
 function AutoMove(a, b, t)
 	output = a
 	if a == b then
@@ -197,18 +162,10 @@
 	return output
 end
 
----Return the Distance between the numbers `a` and `b`
----@param a number
----@param b number
----@return number
 function AutoDist(a, b)
 	return math.abs(a - b)
 end
 
----Normalizes all values in a table to have a magnitude of 1 - Scales every number to still represent the same "direction"
----@param t table<number>
----@param scale number?
----@return table
 function AutoNormalize(t, scale)
 	local norm = {}
 	local maxabs = 0
@@ -223,13 +180,6 @@
 	return norm
 end
 
----Takes a table of weights, like {1, 2, 0.5, 0.5}, and produces a table of how much space each weight would take up if it were to span over a given length.
----If given the weights {1, 2, 0.5, 0.5}, with a span length of 100, the resulting table would be = {25, 50, 12.5, 12.5}.
----A padding parameter can also be added which can be used to make Ui easier. Iterate through the resulting table, after each UiRect, move the width + the padding parameter
----@param weights table<number>|number weights
----@param span number
----@param padding number?
----@return table
 function AutoFlex(weights, span, padding)
 	local istable = type(weights) == "table"
 	weights = not istable and (function()
@@ -259,9 +209,6 @@
 	return flexxed
 end
 
----Returns index of the selected weight using a bias based on the weight values. Good for Biased Randomness
----@param weights table<number>
----@return number selected
 function AutoBias(weights)
 	local T = {}
 	local max = 0
@@ -285,27 +232,7 @@
 		end
 	end
 end
---#endregion
---#region Vector Functions
-
----Rebuilds a table in a given order, also known as Swizzling
----
----| Swizzle | Result |
----| --- | --- |
----| `xyz` | { x, y, z } |
----| `zxy` | { z, x, y } |
----| `xy` | { x, y } |
----| `xz` | { x, z } |
----| `xxx` | { x, x, x } |
----| `xyzw` | { x, y, z, w } |
----| `wxyz` | { w, x, y, z } |
----| `rgba` | { r, g, b, a } |
----| `bgra` | { b, g, r, a } |
----| `aaaa` | { a, a, a, a } |
----
----@param vec vector|table
----@param swizzle string
----@return table
+
 function AutoSwizzle(vec, swizzle)
 	local swizzleMap = { x = 1, y = 2, z = 3, w = 4, r = 1, g = 2, b = 3, a = 4 }
 	local built = {}
@@ -317,10 +244,6 @@
 	return built
 end
 
----Returns true if each axis of vector `a` is equal to each axis of vector `b`
----@param a vector
----@param b vector
----@return boolean
 function AutoVecEquals(a, b)
 	for i, va in pairs(a) do
 		if va ~= b[i] then return false end
@@ -329,10 +252,6 @@
 	return true
 end
 
----Return a Random Vector with an optional offset and scale
----@param param1 number|vector
----@param param2 number?
----@return vector
 function AutoVecRnd(param1, param2)
 	local offset, scale
 	if type(param1) == "table" then
@@ -353,88 +272,42 @@
 	return v
 end
 
----Return the Distance between Two Vectors
----@param a vector
----@param b vector
----@return number
 function AutoVecDist(a, b)
 	return VecLength(VecSub(b, a))
 end
 
----Return the Distance between Two Vectors, without considering the X component
----@param a vector
----@param b vector
----@return number
 function AutoVecDistNoX(a, b)
 	return math.sqrt((b[2] - a[2])^2 + (b[3] - a[3])^2)
 end
 
----Return the Distance between Two Vectors, without considering the Y component
----@param a vector
----@param b vector
----@return number
 function AutoVecDistNoY(a, b)
 	return math.sqrt((b[1] - a[1])^2 + (b[3] - a[3])^2)
 end
 
----Return the Distance between Two Vectors, without considering the Z component
----@param a vector
----@param b vector
----@return number
 function AutoVecDistNoZ(a, b)
 	return math.sqrt((b[1] - a[1])^2 + (b[2] - a[2])^2)
 end
 
----Moves a vector in a direction by a given amount
----
----Equivalent to `VecAdd(vec, VecScale(dir, dist))`
----@param vec any
----@param dir any
----@param dist any
----@return vector
 function AutoVecMove(vec, dir, dist)
 	return VecAdd(vec, VecScale(dir, dist))
 end
 
----Returns a Vector Rounded to a number
----@param vec vector
----@param r number?
----@return vector
 function AutoVecRound(vec, r)
 	return Vec(AutoRound(vec[1], r), AutoRound(vec[2], r), AutoRound(vec[3], r))
 end
 
----Returns a Vector where all numbers are floored
----@param vec vector
----@return vector
 function AutoVecFloor(vec)
 	return Vec(math.floor(vec[1]), math.floor(vec[2]), math.floor(vec[3]))
 end
 
----Returns a Vector where all numbers are ceiled
----@param vec vector
----@return vector
 function AutoVecCeil(vec)
 	return Vec(math.ceil(vec[1]), math.ceil(vec[2]), math.ceil(vec[3]))
 end
 
----Return a vector that has the magnitude of `b`, but with the direction of `a`
----
----Equivalent to `VecScale(VecNormalize(a), b)`
----@param a vector
----@param b number
----@return vector
 function AutoVecRescale(a, b)
 	return VecScale(VecNormalize(a), b)
 end
 
----Maps a Vector from range a1-a2 to range b1-b2
----@param v vector Input Vector
----@param a1 number Goes from the range of number a1
----@param a2 number To number a2
----@param b1 number To the range of b1
----@param b2 number To number b2
----@return vector
 function AutoVecMap(v, a1, a2, b1, b2)
 	if a1 == a2 then return AutoVecRescale(v, b2) end
 	local out = {
@@ -445,11 +318,6 @@
 	return out
 end
 
----Limits the magnitude of a vector to be between min and max
----@param v vector The Vector to clamp
----@param min number? The minimum the magnitude can be, Default is 0
----@param max number? The maximum the magnitude can be, Default is 1
----@return vector
 function AutoVecClampMagnitude(v, min, max)
 	min, max = AutoDefault(min, 0), AutoDefault(max, 1)
 	local l = VecLength(v)
@@ -462,11 +330,6 @@
 	end
 end
 
----Limits a vector to be between min and max
----@param v vector The Vector to clamp
----@param min number? The minimum, Default is 0
----@param max number? The maximum, Default is 1
----@return vector
 function AutoVecClamp(v, min, max)
 	min, max = AutoDefault(min, 0), AutoDefault(max, 1)
 	return {
@@ -476,27 +339,14 @@
 	}
 end
 
----Return Vec(1, 1, 1) scaled by length
----@param length number return the vector of size length, Default is 1
----@return vector
 function AutoVecOne(length)
 	return VecScale(Vec(1, 1, 1), length or 1)
 end
 
----Returns the midpoint between two vectors
----
----Equivalent to `VecScale(VecAdd(a, b), 0.5)`
----@param a any
----@param b any
----@return vector
 function AutoVecMidpoint(a, b)
 	return VecScale(VecAdd(a, b), 0.5)
 end
 
----Return Vec `a` multiplied by Vec `b`
----@param a vector
----@param b vector
----@return vector
 function AutoVecMulti(a, b)
 	return {
 		a[1] * b[1],
@@ -505,10 +355,6 @@
 	}
 end
 
----Return Vec `a` divided by Vec `b`
----@param a vector
----@param b vector
----@return vector
 function AutoVecDiv(a, b)
 	return {
 		a[1] / b[1],
@@ -517,10 +363,6 @@
 	}
 end
 
----Return Vec `a` to the Power of `b`
----@param a vector
----@param b number
----@return vector
 function AutoVecPow(a, b)
 	return {
 		a[1] ^ b,
@@ -529,10 +371,6 @@
 	}
 end
 
----Return Vec `a` to the Power of Vec `b`
----@param a vector
----@param b vector
----@return vector
 function AutoVecPowVec(a, b)
 	return {
 		a[1] ^ b[1],
@@ -541,9 +379,6 @@
 	}
 end
 
----Returns the absolute value of an vector
----@param v vector
----@return vector
 function AutoVecAbs(v)
 	return {
 		math.abs(v[1]),
@@ -552,77 +387,45 @@
 	}
 end
 
----Equivalent to `math.min(unpack(v))`
----@param v vector
----@return number
 function AutoVecMin(v)
 	return math.min(unpack(v))
 end
 
----Equivalent to `math.max(unpack(v))`
----@param v vector
----@return number
 function AutoVecMax(v)
 	return math.max(unpack(v))
 end
 
---- Rotates a vector around an axis by a given angle
---- @param vec vector The vector to rotate
---- @param axis vector The rotation axis, a unit vector
---- @param angle number The rotation angle in degrees
---- @return vector vec The rotated vector
 function AutoVecRotate(vec, axis, angle)
 	local quat = QuatAxisAngle(axis, angle)
 	return QuatRotateVec(quat, vec)
 end
 
----Return `v` with it's `x` value replaced by `subx`
----@param v vector
----@param subx number
 function AutoVecSubsituteX(v, subx)
 	local new = VecCopy(v)
 	new[1] = subx
 	return new
 end
 
----Return `v` with it's `y` value replaced by `suby`
----@param v vector
----@param suby number
 function AutoVecSubsituteY(v, suby)
 	local new = VecCopy(v)
 	new[2] = suby
 	return new
 end
 
----Return `v` with it's `z` value replaced by `subz`
----@param v vector
----@param subz number
 function AutoVecSubsituteZ(v, subz)
 	local new = VecCopy(v)
 	new[3] = subz
 	return new
 end
 
----Converts the output of VecDot with normalized vectors to an angle
----@param dot number
----@return number
 function AutoDotToAngle(dot)
 	return math.deg(math.acos(dot))
 end
 
---#endregion
---#region Quat Functions
-
----Equivalent to `QuatRotateVec(rot, Vec(0, 0, 1))`
----@param rot quaternion
----@return vector
 function AutoQuatFwd(rot)
 	return QuatRotateVec(rot, Vec(0, 0, 1))
 end
 
----Returns a random quaternion
----@param angle number degrees
----@return quaternion
 function AutoRandomQuat(angle)
 	local axis = { math.random() - 0.5, math.random() - 0.5, math.random() - 0.5 }
 	local sinHalfAngle = math.sin(math.rad(angle) / 2)
@@ -635,45 +438,24 @@
 )
 end
 
----Computes the dot product of two quaternions.
----@param a quaternion
----@param b quaternion
----@return number
 function AutoQuatDot(a, b)
 	return a[1] * b[1] + a[2] * b[2] + a[3] * b[3] + a[4] * b[4]
 end
 
----Returns the Conjugate of the given quaternion.
----@param quat quaternion
----@return quaternion quat
 function AutoQuatConjugate(quat)
 	return { -quat[1], -quat[2], -quat[3], quat[4] }
 end
 
----Returns the Inverse of the given quaternion.
----@param quat quaternion
----@return quaternion quat
 function AutoQuatInverse(quat)
 	local norm = quat[1] ^ 2 + quat[2] ^ 2 + quat[3] ^ 2 + quat[4] ^ 2
 	local inverse = { -quat[1] / norm, -quat[2] / norm, -quat[3] / norm, quat[4] / norm }
 	return inverse
 end
 
----Between -a and a, picks the quaternion nearest to b
----@param a quaternion
----@param b quaternion
----@return quaternion
----
----Thankyou to Mathias for this function
 function AutoQuatNearest(a, b)
 	return AutoQuatDot(a, b) < 0 and { -a[1], -a[2], -a[3], -a[4] } or { a[1], a[2], a[3], a[4] }
 end
 
----Same as `QuatAxisAngle()` but takes a single vector instead of a unit vector + an angle, for convenience
----
----Thankyou to Mathias for this function
----@param v any
----@return quaternion
 function AutoQuatFromAxisAngle(v)
 	local xyz = VecScale(v, 0.5)
 	local angle = VecLength(xyz)
@@ -688,10 +470,6 @@
 	return Quat(qXYZ[1], qXYZ[2], qXYZ[3], co)
 end
 
----Converts a quaternion to an axis angle representation
----Returns a rotation vector where axis is the direction and angle is the length
----
----Thankyou to Mathias for this function
 function AutoQuatToAxisAngle(q)
 	local qXYZ = Vec(q[1], q[2], q[3])
 	local co = q[4]
@@ -705,31 +483,16 @@
 	return VecScale(qXYZ, 2.0 * angle / si)
 end
 
---#endregion
---#region AABB Bounds Functions
-
----Get the center of a body's bounds
----@param body body_handle
----@return vector
 function AutoBodyCenter(body)
 	local aa, bb = GetBodyBounds(body)
 	return VecScale(VecAdd(aa, bb), 0.5)
 end
 
----Get the center of a shapes's bounds
----@param shape shape_handle
----@return vector
 function AutoShapeCenter(shape)
 	local aa, bb = GetShapeBounds(shape)
 	return VecScale(VecAdd(aa, bb), 0.5)
 end
 
----Expands a given boudns to include a point
----@param aa vector
----@param bb vector
----@param ... vector Points, can be one or multiple
----@return vector
----@return vector
 function AutoAABBInclude(aa, bb, ...)
 	for _, point in ipairs(arg) do
 		aa, bb = {
@@ -746,11 +509,6 @@
 	return aa, bb
 end
 
----Returns a Axis ALigned Bounding Box with the center of pos
----@param pos vector
----@param halfextents vector|number
----@return vector lower-bound
----@return vector upper-bound
 function AutoAABBBoxFromPoint(pos, halfextents)
 	if type(halfextents) == "number" then
 		halfextents = AutoVecOne(halfextents)
@@ -759,11 +517,6 @@
 	return VecSub(pos, halfextents), VecAdd(pos, halfextents)
 end
 
----Takes two vectors and modifys them so they can be used in other bound functions
----@param aa vector
----@param bb vector
----@return vector
----@return vector
 function AutoAABBCorrection(aa, bb)
 	local min, max = VecCopy(aa), VecCopy(bb)
 	
@@ -783,11 +536,6 @@
 	return min, max
 end
 
----Get a position inside or on the Input Bounds
----@param aa vector lower-bound
----@param bb vector upper-bound
----@param vec vector? A normalized Vector pointing towards the position that should be retrieved, Default is Vec(0, 0, 0)
----@return vector
 function AutoAABBGetPos(aa, bb, vec)
 	vec = AutoDefault(vec, Vec(0, 0, 0))
 	
@@ -799,10 +547,6 @@
 	return VecAdd(scaled, aa)
 end
 
----Get the corners of the given Bounds
----@param aa vector lower-bound
----@param bb vector upper-bound
----@return table
 function AutoAABBGetCorners(aa, bb)
 	local mid = {}
 	for i = 1, 3 do
@@ -823,12 +567,6 @@
 	return corners
 end
 
----Get data about the size of the given Bounds
----@param aa vector lower-bound
----@param bb vector upper-bound
----@return table representing the size of the Bounds
----@return number smallest smallest edge size of the Bounds
----@return number longest longest edge size of the Bounds
 function AutoAABBSize(aa, bb)
 	local size = VecSub(bb, aa)
 	local minval = math.min(unpack(size))
@@ -837,11 +575,6 @@
 	return size, minval, maxval
 end
 
----Takes a given AABB and subdivides into new AABBs
----@param aa vector lower-bound
----@param bb vector upper-bound
----@param levels number?
----@return table
 function AutoAABBSubdivideBounds(aa, bb, levels)
 	levels = levels or 1
 	local bounds = { { aa, bb } }
@@ -871,15 +604,6 @@
 	return bounds
 end
 
----Draws a given Axis Aligned Bounding Box
----@param aa vector lower-bound
----@param bb vector upper-bound
----@param colorR number?
----@param colorG number?
----@param colorB number?
----@param alpha number?
----@param rgbcolors boolean?
----@param draw boolean?
 function AutoDrawAABB(aa, bb, colorR, colorG, colorB, alpha, rgbcolors, draw)
 	colorR = AutoDefault(colorR, 0)
 	colorG = AutoDefault(colorG, 0)
@@ -931,26 +655,12 @@
 	end
 end
 
---#endregion
---#region OBB Bounds Functions
-
----@class OBB: { pos:vector, rot:quaternion, size:vector }|transform
-
----Converts an Axis Aligned Bounding Box to a Oriented Bounding Box
----@param aa vector
----@param bb vector
----@return OBB
 function AutoAABBToOBB(aa, bb)
 	local center = VecLerp(bb, aa, 0.5)
 	local size = VecSub(bb, aa)
 	return { pos = center, rot = QuatEuler(), size = size }
 end
 
----Defines a Oriented Bounding Box
----@param center vector
----@param rot quaternion
----@param size vector|number?
----@return table
 function AutoOBB(center, rot, size)
 	return {
 		pos = center or Vec(),
@@ -959,9 +669,6 @@
 	}
 end
 
----Returns the corners of a Oriented Bounding Box
----@param obb OBB
----@return { xyz:table, Xyz:table, xYz:table, xyZ:table, XYz:table, XyZ:table, xYZ:table, XYZ:table }
 function AutoGetOBBCorners(obb)
 	local corners = {}
 	
@@ -979,10 +686,6 @@
 	return corners
 end
 
----Returns the planes and corners representing the faces of a Oriented Bounding Box
----@param obb OBB
----@return { z:plane, zn:plane, x:plane, xn:plane, y:plane, yn:plane }
----@return { xyz:table, Xyz:table, xYz:table, xyZ:table, XYz:table, XyZ:table, xYZ:table, XYZ:table }
 function AutoGetOBBFaces(obb)
 	local corners = AutoGetOBBCorners(obb)
 	
@@ -1021,9 +724,6 @@
 	return faces, corners
 end
 
----Returns a table representing the lines connecting the sides of a Oriented Bounding Box
----@param obb OBB
----@return table<{ [1]:vector, [2]:vector }>
 function AutoOBBLines(obb)
 	local c = AutoGetOBBCorners(obb)
 	
@@ -1045,8 +745,6 @@
 	}
 end
 
----@param shape shape_handle
----@return OBB
 function AutoGetShapeOBB(shape)
 	local transform = GetShapeWorldTransform(shape)
 	local x, y, z, scale = GetShapeSize(shape)
@@ -1056,13 +754,6 @@
 	return AutoOBB(center, transform.rot, size)
 end
 
----Draws a given Oriented Bounding Box
----@param obb OBB
----@param red number? Default is 0
----@param green number? Default is 0
----@param blue number? Default is 0
----@param alpha number? Default is 1
----@param linefunction function? Default is DebugLine
 function AutoDrawOBB(obb, red, green, blue, alpha, linefunction)
 	local lines = AutoOBBLines(obb)
 	
@@ -1072,21 +763,10 @@
 	end
 end
 
---#endregion
---#region Plane Functions
-
----@class plane: { pos:vector, rot:quaternion, size:{ [1]:number, [2]:number } }|transform
-
----@param pos vector
----@param rot quaternion
----@param size { [1]:number, [2]:number }
----@return plane
 function AutoPlane(pos, rot, size)
 	return { pos = pos or Vec(), rot = rot or Quat(), size = size or { 1, 1 } }
 end
 
----@param plane plane
----@return { [1]:vector, [2]:vector, [3]:vector, [4]:vector }
 function AutoGetPlaneCorners(plane)
 	local size = VecScale(plane.size, 0.5)
 	
@@ -1104,11 +784,6 @@
 	return { corner1, corner2, corner3, corner4 }
 end
 
----@param plane plane
----@param startPos vector
----@param direction vector
----@param oneway boolean?
----@return { hit:boolean, intersection:vector, normal:vector, dist:number, dot:number }
 function AutoRaycastPlane(plane, startPos, direction, oneway)
 	local pos = plane.pos or Vec(0, 0, 0)
 	local rot = plane.rot or Quat()
@@ -1165,9 +840,6 @@
 	end
 end
 
----@param startPos vector
----@param direction vector
----@return { hit:boolean, intersections:{ [1]:vector, [2]:vector }, normals:{ [1]:vector, [2]:vector }, dists:{ [1]:number, [2]:number } }
 function AutoRaycastSphere(sphere_origin, sphere_radius, startPos, direction)
     local center = sphere_origin or Vec(0, 0, 0)
     local radius = sphere_radius or 1
@@ -1217,15 +889,6 @@
     }
 end
 
----@param plane plane
----@param pattern 0|1|2|3
----@param patternstrength number
----@param oneway boolean?
----@param r number?
----@param g number?
----@param b number?
----@param a number?
----@param linefunction function?
 function AutoDrawPlane(plane, pattern, patternstrength, oneway, r, g, b, a, linefunction)
 	local pos = plane.pos or Vec(0, 0, 0)
 	local rot = plane.rot or Quat()
@@ -1265,7 +928,7 @@
 			linefunction(subH1, subH2, r, g, b, a)
 			linefunction(subV1, subV2, r, g, b, a)
 		end
-	elseif pattern > 0 then
+	elseif pattern ~= 0 then
 		linefunction(corner1, corner2, r, g, b, a)
 		linefunction(corner2, corner3, r, g, b, a)
 		linefunction(corner3, corner4, r, g, b, a)
@@ -1300,16 +963,6 @@
 	end
 end
 
---#endregion
---#region Octree Functions
-
----Undocumented
----@param BoundsAA vector
----@param BoundsBB vector
----@param Layers number
----@param conditionalFuction function
----@param _layer number?
----@return table
 function AutoProcessOctree(BoundsAA, BoundsBB, Layers, conditionalFuction, _layer)
 	_layer = _layer or 1
 	if _layer >= (Layers or 5) + 1 then return end
@@ -1336,11 +989,6 @@
 	return node
 end
 
----Undocumented
----@param aa vector
----@param bb vector
----@return boolean
----@return table
 function AutoQueryBoundsForBody(aa, bb)
 	QueryRequire('physical large')
 	local mid = VecLerp(aa, bb, 0.5)
@@ -1349,10 +997,6 @@
 	return hit, { pos = point, normal = normal, shape }
 end
 
----Draws the Octree from AutoProcessOctree
----@param node table
----@param layer number
----@param drawfunction function?
 function AutoDrawOctree(node, layer, drawfunction)
 	if node == nil then return end
 	
@@ -1376,10 +1020,6 @@
 	end
 end
 
---#endregion
---#region Point Physics
-
----Creates a Point Physics Simulation Instance
 function AutoSimInstance()
 	local t = {
 		Points = {
@@ -1550,21 +1190,6 @@
 	return t
 end
 
---#endregion
---#region Secondary Motion
-
---Previously known as Second Order System
---Huge Thanks to Mathias#1325 for work on the Quaternion Functions
-
----@class Secondary_Motion_Data: table
-
----Returns a table representing a Second Order System (SOS) that can be used to make secondary motion
----@param initial number|table<number>
----@param frequency number
----@param dampening number
----@param response number
----@param raw_k boolean?
----@return Secondary_Motion_Data
 function AutoSM_Define(initial, frequency, dampening, response, raw_k)
 	local sosdata = {
 		type = type(initial) == 'table' and 'table' or 'single',
@@ -1596,13 +1221,6 @@
 	return sosdata
 end
 
----Returns a table representing a Second Order System (SOS) that can be used to make secondary motion
----@param initial number|table<number>
----@param frequency number
----@param dampening number
----@param response number
----@param raw_k boolean?
----@return Secondary_Motion_Data
 function AutoSM_DefineQuat(initial, frequency, dampening, response, raw_k)
 	local sosdata = {
 		type = 'quaternion',
@@ -1621,11 +1239,6 @@
 	return sosdata
 end
 
----Updates the state of the Second Order System (SOS) towards the target value, over the specified timestep.
----This function is used in conjunction with the AutoSM_Define
----@param sm Secondary_Motion_Data
----@param target number|table<number>
----@param timestep number?
 function AutoSM_Update(sm, target, timestep)
 	timestep = timestep or GetTimeStep()
 	
@@ -1671,9 +1284,6 @@
 	end
 end
 
----Returns the current value of a Second Order System
----@param sm Secondary_Motion_Data
----@return number|table<number>|quaternion
 function AutoSM_Get(sm)
 	if sm.type ~= 'table' then
 		return sm.data.current
@@ -1687,9 +1297,6 @@
 	end
 end
 
----Returns the current velocity of a Second Order System
----@param sm Secondary_Motion_Data
----@return number|table<number>
 function AutoSM_GetVelocity(sm)
 	if sm.type ~= 'table' then
 		return sm.data.velocity
@@ -1698,10 +1305,6 @@
 	end
 end
 
----Sets the current values of a Second Order System
----@param sm Secondary_Motion_Data
----@param target number|table<number>|quaternion
----@param keep_velocity boolean?
 function AutoSM_Set(sm, target, keep_velocity)
 	if sm.type ~= 'table' then
 		sm.data.current = target
@@ -1722,9 +1325,6 @@
 	end
 end
 
----Sets the current velocity of a Second Order System
----@param sm Secondary_Motion_Data
----@param velocity number|table<number>
 function AutoSM_SetVelocity(sm, velocity)
 	if sm.type == 'single' then
 		sm.data.velocity = velocity
@@ -1737,9 +1337,6 @@
 	end
 end
 
----Adds a amount to the current velocity of a Second Order System
----@param sm Secondary_Motion_Data
----@param velocity number|table<number>
 function AutoSM_AddVelocity(sm, velocity)
 	if sm.type == 'single' then
 		sm.data.velocity = sm.data.velocity + velocity
@@ -1752,12 +1349,6 @@
 	end
 end
 
----Recalculates The K values for a Second Order System
----@param sm Secondary_Motion_Data
----@param frequency number
----@param dampening number
----@param response number
----@param raw_k boolean?
 function AutoSM_RecalculateK(sm, frequency, dampening, response, raw_k)
 	sm.k_values = {
 		raw_k and frequency or (dampening / (math.pi * frequency)),
@@ -1766,12 +1357,6 @@
 	}
 end
 
---#endregion
---#region Table Functions
-
----Returns the amount of elements in the given list.
----@param t table
----@return integer
 function AutoTableCount(t)
 	local c = 0
 	for i in pairs(t) do
@@ -1781,10 +1366,6 @@
 	return c
 end
 
----Repeats a value `v`, `r` amount of times
----@param v any
----@param r integer
----@return table
 function AutoTableRepeatValue(v, r)
 	local t = {}
 	for i=1,r do
@@ -1793,9 +1374,6 @@
 	return t
 end
 
----Concats Table 2 onto the end of Table 1, does not return anything
----@param t1 table
----@param t2 table
 function AutoTableConcat(t1, t2, reverse)
 	if not reverse then
 		for i = 1, #t2 do
@@ -1808,9 +1386,6 @@
 	end
 end
 
----Merges two tables together, does not return anything
----@param base table
----@param overwrite table
 function AutoTableMerge(base, overwrite)
 	for k, v in pairs(overwrite) do
 		if type(v) == "table" then
@@ -1825,10 +1400,6 @@
 	end
 end
 
----A lambda like function for returning a table's key's values.
----@param t table
----@param key any
----@return table
 function AutoTableSub(t, key)
 	local _t = {}
 	for i, v in pairs(t) do
@@ -1837,11 +1408,6 @@
 	return _t
 end
 
----A lambda like function for returning a table's key's values.
----Same as AutoTableSub, but uses ipairs instead
----@param t table
----@param key any
----@return table
 function AutoTableSubi(t, key)
 	local _t = {}
 	for i, v in ipairs(t) do
@@ -1850,9 +1416,6 @@
 	return _t
 end
 
----Swaps the keys and the values of a table
----@param t table
----@return table
 function AutoTableSwapKeysAndValues(t)
 	local _t = {}
 	for k, v in pairs(t) do
@@ -1861,25 +1424,12 @@
 	return _t
 end
 
----Equivalent to
----```
----for i, v in pairs(t) do
----    v[key] = tset[i]
----end
----```
----@param t table
----@param key any
----@param tset table
 function AutoTableAppend(t, key, tset)
 	for i, v in pairs(t) do
 		v[key] = tset[i]
 	end
 end
 
----Returns true and the index if the v is in t, otherwise returns false and nil
----@param t table
----@param v any
----@return boolean, unknown
 function AutoTableContains(t, v)
 	for i, v2 in ipairs(t) do
 		if v == v2 then
@@ -1889,18 +1439,10 @@
 	return false, nil
 end
 
----Returns the Last item of a given list
----@param t table
----@return any
 function AutoTableLast(t)
 	return t[AutoTableCount(t)]
 end
 
----Copy a Table Recursivly Stolen from http://lua-users.org/wiki/CopyTable
----@generic T : table
----@param orig T
----@param copies table?
----@return T
 function AutoTableDeepCopy(orig, copies)
 	copies = copies or {}
 	local orig_type = type(orig)
@@ -1922,20 +1464,10 @@
 	return copy
 end
 
---#endregion
---#region Utility Functions
-
----If val is nil, return default instead
----@param v any
----@param default any
----@return any
 function AutoDefault(v, default)
 	if v == nil then return default else return v end
 end
 
----Calls function or table of functions `f` and gives `...` as input parameters
----@param f function|table<function>
----@vararg any
 function AutoExecute(f, ...)
 	if not f then return end
 	
@@ -1950,11 +1482,6 @@
 	end
 end
 
----Calls VecLerp on a table of Vectors
----@param a table A table of Vectors
----@param b table A table of Vectors the same size of a
----@param t number
----@return table
 function AutoVecTableLerp(a, b, t)
 	local c = {}
 	for k, _ in pairs(a) do
@@ -1963,11 +1490,6 @@
 	return c
 end
 
----Calls VecLerp on a table of Vectors
----@param a table A table of values
----@param b table A table of values the same size of a
----@param t number
----@return table
 function AutoTableLerp(a, b, t)
 	local c = {}
 	for k, _ in pairs(a) do
@@ -1976,21 +1498,10 @@
 	return c
 end
 
----Scales a transform, is the equivelent of (s)lerping the position and rotation from Vec(), Quat()
----@param t transform
----@param s number
----@param s2 number?
----@return transform
 function AutoTransformScale(t, s, s2)
 	return AutoTransformLerp(Transform(Vec(), Quat()), t, s, s2)
 end
 
----Returns a Linear Interpolated Transform, Interpolated by t.
----@param a transform
----@param b transform
----@param t number
----@param t2 number?
----@return table
 function AutoTransformLerp(a, b, t, t2)
 	if t2 == nil then
 		t2 = t
@@ -2001,58 +1512,31 @@
 )
 end
 
----Equivalent to `QuatRotateVec(t.rot, Vec(0, 0, -(scale or 1)))`
----@param t transform
----@param scale number?
----@return vector
 function AutoTransformFwd(t, scale)
 	return QuatRotateVec(t.rot, Vec(0, 0, -(scale or 1)))
 end
 
----Equivalent to `QuatRotateVec(t.rot, Vec(0, scale or 1))`
----@param t transform
----@param scale number?
----@return vector
 function AutoTransformUp(t, scale)
 	return QuatRotateVec(t.rot, Vec(0, scale or 1))
 end
 
----Equivalent to `QuatRotateVec(t.rot, Vec(scale or 1))`
----@param t transform
----@param scale number?
----@return vector
 function AutoTransformRight(t, scale)
 	return QuatRotateVec(t.rot, Vec(scale or 1))
 end
 
----Equivalent to `Transform(TransformToParentPoint(t, offset), t.rot)`
----@param t transform
----@param offset vector
----@return transform
 function AutoTransformOffset(t, offset)
 	return Transform(TransformToParentPoint(t, offset), t.rot)
 end
 
----Equivalent to `{ GetQuatEuler(quat) }`
----@param quat quaternion
----@return vector
 function AutoEulerTable(quat)
 	return { GetQuatEuler(quat) }
 end
 
----Returns a Vector for easy use when put into a parameter for xml
----@param vec any
----@param round number
----@return string
 function AutoVecToXML(vec, round)
 	round = AutoDefault(round, 0)
 	return AutoRound(vec[1], round) .. ' ' .. AutoRound(vec[2], round) .. ' ' .. AutoRound(vec[3], round)
 end
 
----Splits a string by a separator
----@param inputstr string
----@param sep string
----@return table
 function AutoSplit(inputstr, sep, number)
 	if sep == nil then
 		sep = "%s"
@@ -2064,19 +1548,11 @@
 	return t
 end
 
----Converts a string to be capitalized following the Camel Case pattern
----@param str string
----@return string
 function AutoCamelCase(str)
 	local subbed = str:gsub('_', ' ')
 	return string.gsub(" " .. subbed, "%W%l", string.upper):sub(2)
 end
 
----Returns 3 values from HSV color space from RGB color space
----@param hue number? The hue from 0 to 1
----@param sat number? The saturation from 0 to 1
----@param val number? The value from 0 to 1
----@return number, number, number Returns the red, green, blue of the given hue, saturation, value
 function AutoHSVToRGB(hue, sat, val)
 	local r, g, b
 	
@@ -2099,11 +1575,6 @@
 	return r, g, b
 end
 
----Returns 3 values from RGB color space from HSV color space
----@param r number? The red from 0 to 1
----@param g number? The green from 0 to 1
----@param b number? The blue from 0 to 1
----@return number, number, number Returns the hue, the saturation, and the value
 function AutoRGBToHSV(r, g, b)
 	r, g, b = r, g, b
 	local max, min = math.max(r, g, b), math.min(r, g, b)
@@ -2128,9 +1599,6 @@
 	return h, s, v
 end
 
----Converts a hex code or a table of hex codes to RGB color space
----@param hex string|table<string>
----@return number|table
 function AutoHEXtoRGB(hex)
 	local function f(x, p)
 		x = x:gsub("#", "")
@@ -2148,11 +1616,6 @@
 	end
 end
 
----Converts an RGB color code or a table of RGB color codes to hexadecimal color space
----@param r number|table<number> Red component (0-1) or table of RGB color codes
----@param g number Green component (0-1) (optional)
----@param b number Blue component (0-1) (optional)
----@return string|table<string> Hexadecimal color code or table of hex codes
 function AutoRGBtoHEX(r, g, b)
 	local function f(x)
 		local hx = string.format("%02X", math.floor(x * 255))
@@ -2172,9 +1635,6 @@
 	end
 end
 
----Performs `:byte()` on each character of a given string
----@param str string
----@return table<number>
 function AutoStringToByteTable(str)
 	local t = {}
 	for i = 1, #str do
@@ -2183,11 +1643,6 @@
 	return t
 end
 
----Performs `:char()` on each number of a given table, returning a string
----
----The inverse of AutoStringToByteTable
----@param t table<number>
----@return string
 function AutoByteTableToString(t)
 	local str = ''
 	for i, b in ipairs(t) do
@@ -2196,18 +1651,12 @@
 	return str
 end
 
---#endregion
---#region Game Functions
-
----Usually, the Primary Menu Button only is suppose to work in the mod's level, this is a work around to have it work in any level.
----@param title string
----@return boolean
 function AutoPrimaryMenuButton(title)
 	local value = PauseMenuButton(title, true)
 	
 	for _, item in pairs(ListKeys('game.pausemenu.items')) do
 		if GetString(AutoKey('game.pausemenu.items', item)) == title then
-			SetInt('game.pausemenu.primary', item)
+			SetInt('game.pausemenu.primary', item, true)
 			break
 		end
 	end
@@ -2215,10 +1664,6 @@
 	return value
 end
 
----Goes through a table and performs Delete() on each element
----@param t table<entity_handle>
----@param CheckIfValid boolean?
----@return table<{handle:entity_handle, type:entity_type, valid:boolean}>
 function AutoDeleteHandles(t, CheckIfValid)
 	local list = {}
 	for k, v in pairs(t) do
@@ -2249,10 +1694,6 @@
 	end
 end
 
-
----Creates a list from a table of entity handles, containing the handle and it's type. If the handle is invalid then the type will be false.
----@param t table<entity_handle>
----@return table<{handle:entity_handle, type:entity_type}>
 function AutoListHandleTypes(t)
 	local nt = {}
 	for key, value in pairs(t) do
@@ -2261,30 +1702,17 @@
 	return nt
 end
 
----Spawn in a script node in the game world.
----@param path td_path
----@param ... string|number?
----@return script_handle
 function AutoSpawnScript(path, ...)
 	local f = [[<script file="%s" param0="%s" param1="%s" param2="%s" param3="%s"/>]]
 	local param = { arg[1] or '', arg[2] or '', arg[3] or '', arg[4] or '' }
 	return Spawn((f):format(path, unpack(param)), Transform())[1]
 end
 
----Spawn in a voxscript node in the game world. No parameters
----@param path td_path
----@return script_handle
 function AutoSpawnVoxScript(path)
 	local f = [[<voxscript file="%s"/>]]
 	return Spawn((f):format(path), Transform())[1]
 end
 
----Attempts to get the handle of the current script by abusing pause menu item keys
----
----May not work if a pause menu button is already being created from the script
----
----Original coded from Thomasims
----@return script_handle
 function AutoGetScriptHandle()
 	local id = tostring(math.random())
 	PauseMenuButton(id)
@@ -2297,13 +1725,6 @@
 	end
 end
 
----A Wrapper for QueryRaycast; comes with some extra features.
----@param origin vector
----@param direction vector
----@param maxDist number
----@param radius number?
----@param rejectTransparent boolean?
----@return { hit:boolean, intersection:vector, dist:number, normal:vector, shape:shape_handle, body:body_handle, dir:vector, dot:number, reflection:vector }
 function AutoRaycast(origin, direction, maxDist, radius, rejectTransparent)
 	direction = direction and VecNormalize(direction) or nil
 	
@@ -2318,37 +1739,18 @@
 	return data
 end
 
----AutoRaycast from point A to point B. The distance will default to the distance between the points, but can be set.
----@param pointA vector
----@param pointB vector
----@param manualDistance number?
----@param radius number?
----@param rejectTransparent boolean?
----@return { hit:boolean, dist:number, normal:vector, shape:shape_handle, intersection:vector, body:body_handle, dir:vector, dot:number, reflection:vector }
 function AutoRaycastTo(pointA, pointB, manualDistance, radius, rejectTransparent)
 	local diff = VecSub(pointB, pointA)
 	return AutoRaycast(pointA, diff, manualDistance or VecLength(diff), radius, rejectTransparent)
 end
 
----AutoRaycast using the camera or player camera as the origin and direction
----@param usePlayerCamera boolean
----@param maxDist number
----@param radius number?
----@param rejectTransparent boolean?
----@return { hit:boolean, dist:number, normal:vector, shape:shape_handle, intersection:vector, body:body_handle, dir:vector, dot:number, reflection:vector }
----@return transform cameraTransform
----@return vector cameraForward
 function AutoRaycastCamera(usePlayerCamera, maxDist, radius, rejectTransparent)
-	local trans = usePlayerCamera and GetPlayerCameraTransform() or GetCameraTransform()
+	local trans = usePlayerCamera and GetPlayerCameraTransform(playerId) or GetCameraTransform()
 	local fwd = AutoTransformFwd(trans)
 	
 	return AutoRaycast(trans.pos, fwd, maxDist, radius, rejectTransparent), trans, fwd
 end
 
----A Wrapper for QueryClosestPoint; comes with some extra features.
----@param origin vector
----@param maxDist number
----@return { hit:boolean, point:vector, normal:vector, shape:shape_handle, body:body_handle, dist:number, dir:vector, dot:number, reflection:vector }
 function AutoQueryClosest(origin, maxDist)
 	local data = {}
 	data.hit, data.point, data.normal, data.shape = QueryClosestPoint(origin, maxDist)
@@ -2370,10 +1772,6 @@
 	return data
 end
 
----A Wrapper for GetBodyClosestPoint; comes with some extra features.
----@param body body_handle
----@param origin vector
----@return { hit:boolean, point:vector, normal:vector, shape:shape_handle, body:body_handle, dist:number, dir:vector, dot:number, reflection:vector }
 function AutoQueryClosestBody(body, origin)
 	local data = {}
 	data.hit, data.point, data.normal, data.shape = GetBodyClosestPoint(body, origin)
@@ -2393,10 +1791,6 @@
 	return data
 end
 
----A Wrapper for GetShapeClosestPoint; comes with some extra features.
----@param shape shape_handle
----@param origin vector
----@return { hit:boolean, point:vector, normal:vector, dist:number, dir:vector, dot:number, reflection:vector, body:body_handle }
 function AutoQueryClosestShape(shape, origin)
 	local data = {}
 	data.hit, data.point, data.normal = GetShapeClosestPoint(shape, origin)
@@ -2416,9 +1810,6 @@
 	return data
 end
 
----Goes through each shape on a body and adds up their voxel count
----@param body body_handle
----@return integer
 function AutoGetBodyVoxels(body)
 	local v = 0
 	for _, s in pairs(GetBodyShapes(body)) do
@@ -2427,11 +1818,6 @@
 	return v
 end
 
----Scales the velocity of a body by `scale`
----@param body body_handle
----@param scale number
----@return vector scaled
----@return vector orginal
 function AutoScaleBodyVelocity(body, scale)
 	local orginal = GetBodyVelocity(body)
 	local scaled = VecScale(orginal, scale)
@@ -2439,11 +1825,6 @@
 	return scaled, orginal
 end
 
----Scales the angular velocity of a body by `scale`
----@param body body_handle
----@param scale number
----@return vector scaled
----@return vector orginal
 function AutoScaleBodyAngularVelocity(body, scale)
 	local current = GetBodyAngularVelocity(body)
 	local scaled = VecScale(current, scale)
@@ -2451,10 +1832,6 @@
 	return scaled, current
 end
 
----Gets the angle from a point to the forward direction of a transform
----@param point vector
----@param fromtrans transform
----@return number
 function AutoPointToAngle(point, fromtrans)
 	fromtrans = AutoDefault(fromtrans, GetCameraTransform())
 	
@@ -2465,14 +1842,6 @@
 	return math.deg(math.acos(dot))
 end
 
----Checks if a point is in the view using a transform acting as the "Camera"
----@param point vector
----@param oftrans transform? The Transform acting as the camera, Default is the Player's Camera
----@param angle number? The Angle at which the point can be seen from, Default is the Player's FOV set in the options menu
----@param raycastcheck boolean? Check to make sure that the point is not obscured, Default is true
----@return boolean seen If the point is in View
----@return number? angle The Angle the point is away from the center of the looking direction
----@return number? distance The Distance from the point to fromtrans
 function AutoPointInView(point, oftrans, angle, raycastcheck, raycasterror)
 	oftrans = AutoDefault(oftrans, GetCameraTransform())
 	angle = AutoDefault(angle, GetInt('options.gfx.fov'))
@@ -2496,7 +1865,7 @@
 		if raycastcheck then
 			local hit, hitdist = QueryRaycast(oftrans.pos, fromtopointdir, dist, 0, true)
 			if hit then
-				if raycasterror > 0 then
+				if raycasterror ~= 0 then
 					local hitpoint = VecAdd(oftrans.pos, VecScale(fromtopointdir, hitdist))
 					if AutoVecDist(hitpoint, point) > raycasterror then
 						seen = false
@@ -2511,11 +1880,6 @@
 	return seen, dotangle, dist
 end
 
----Gets the direction the player is inputting and creates a vector.
----
----`{ horizontal, 0, -vertical }`
----@param length number?
----@return vector
 function AutoPlayerInputDir(length)
 	return VecScale({
 		-InputValue('left') + InputValue('right'),
@@ -2524,10 +1888,6 @@
 	}, length or 1)
 end
 
----Get the last Path Query as a path of points
----@param precision number The Accuracy
----@return table<vector>
----@return vector "Last Point"
 function AutoRetrievePath(precision)
 	precision = AutoDefault(precision, 0.2)
 	
@@ -2542,8 +1902,6 @@
 	return path, path[#path]
 end
 
----Reject a table of bodies for the next Query
----@param bodies table<body_handle>
 function AutoQueryRejectBodies(bodies)
 	for _, h in pairs(bodies) do
 		if h then
@@ -2552,8 +1910,6 @@
 	end
 end
 
----Reject a table of shapes for the next Query
----@param shapes table<shape_handle>
 function AutoQueryRejectShapes(shapes)
 	for _, h in pairs(shapes) do
 		if h then
@@ -2562,8 +1918,6 @@
 	end
 end
 
----Finds and rejects all shapes that do not have a given tag
----@param tag string
 function AutoRejectShapesWithoutTag(tag)
 	local all = FindShapes(nil, true)
 	local keep = {}
@@ -2576,10 +1930,6 @@
 	end
 end
 
----Set the collision filter for the shapes owned by a body
----@param body body_handle
----@param layer number
----@param masknummber number bitmask
 function AutoSetBodyCollisionFilter(body, layer, masknummber)
 	local shapes = GetBodyShapes(body)
 	for i in pairs(shapes) do
@@ -2587,30 +1937,16 @@
 	end
 end
 
----Get the Center of Mass of a body in World space
----@param body body_handle
----@return vector
 function AutoWorldCenterOfMass(body)
 	local trans = GetBodyTransform(body)
 	local pos = TransformToParentPoint(trans, GetBodyCenterOfMass(body))
 	return pos
 end
 
----Adds the velocity and angualr velocity of a body
----@param body body_handle
----@return number
 function AutoSpeed(body)
 	return VecLength(GetBodyVelocity(body)) + VecLength(GetBodyAngularVelocity(body))
 end
 
----Attempt to predict the position of a body in time
----@param body body_handle
----@param time number
----@param raycast boolean? Check and Halt on Collision, Default is false
----@param funcbefore function?
----@return table<vector> log
----@return vector vel
----@return vector normal
 function AutoPredictPosition(body, time, raycast, funcbefore)
 	raycast = AutoDefault(raycast, false)
 	local point = {
@@ -2644,17 +1980,11 @@
 	return log, point.vel, normal
 end
 
----Attempt to predict the position of the player in time
----@param time number
----@param raycast boolean? Check and Halt on Collision, Default is false
----@return table<vector> log
----@return vector vel
----@return vector normal
 function AutoPredictPlayerPosition(time, raycast)
 	raycast = AutoDefault(raycast, false)
-	local player = GetPlayerTransform(true)
+	local player = GetPlayerTransform(playerId, true)
 	local pos = player.pos
-	local vel = GetPlayerVelocity()
+	local vel = GetPlayerVelocity(playerId)
 	local log = { VecCopy(pos) }
 	local normal = Vec(0, 1, 0)
 	
@@ -2675,9 +2005,6 @@
 	return log, vel, normal
 end
 
---#endregion
---#region Shape Utility
-
 function AutoWorldToShapeVoxelIndex(shape, world_point)
 	local shape_size = { GetShapeSize(shape) }
 	local shape_transform = GetShapeWorldTransform(shape)
@@ -2708,10 +2035,6 @@
 	return body
 end
 
----SplitShape with some extra stuff to put each shape under a dynamic body - copying the velocity of the original shape.
----@param shape shape_handle
----@param removeResidual boolean?
----@return body_handle[]
 function AutoSplitShapeIntoBodies(shape, removeResidual, static)
 	local new_bodies = {}
 
@@ -2722,14 +2045,6 @@
 	return new_bodies
 end
 
----Creates a new shape offset a 1x1x1 voxel in place of an existing voxel.
----@param shape shape_handle
----@param voxel_position vector
----@param keep_original boolean?
----@param no_body boolean?
----@param require_materials material[]?
----@return body_handle|false
----@return shape_handle|false
 function AutoPopVoxel(shape, voxel_position, keep_original, no_body, require_materials)
 	local material = { GetShapeMaterialAtIndex(shape, unpack(voxel_position)) }
 	if material[1] == '' or (require_materials and not AutoTableContains(require_materials, material[1])) then return false, false end
@@ -2769,13 +2084,6 @@
 	return body, new_shape
 end
 
----A function inspired by the Liquify Mod.
----@param shape shape_handle
----@param keep_original boolean?
----@param inherit_tags boolean?
----@param no_bodies boolean?
----@return body_handle[]
----@return shape_handle[]
 function AutoLiquifyShape(shape, keep_original, inherit_tags, no_bodies)
 	local shape_size = { GetShapeSize(shape) }
 
@@ -2868,46 +2176,6 @@
     return popped_bodies, popped_shapes
 end
 
---#endregion
---#region Environment
-
----@class environment
----@field ambience { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field ambient { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field ambientexponent { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field brightness { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field constant { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field exposure { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field fogcolor { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field fogparams { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field fogscale { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field nightlight { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field puddleamount { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field puddlesize { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field rain { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field skybox { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field skyboxbrightness { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field skyboxrot { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field skyboxtint { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field slippery { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field snowamount { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field snowdir { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field snowonground { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field sunbrightness { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field suncolortint { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field sundir { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field sunfogscale { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field sunglare { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field sunlength { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field sunspread { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field waterhurt { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field wetness { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
----@field wind { [1]:any, [2]:any, [3]:any ,[4]:any, [5]:any }
-
----@type environment_property
-
----Returns a table of every property of the current environment
----@return environment
 function AutoGetEnvironment()
 	local params = {
 		"ambient",
@@ -2949,8 +2217,6 @@
 	return assembled
 end
 
----Sets every environment property of AutoGetEnvironment
----@param Environment environment
 function AutoSetEnvironment(Environment)
 	for k, v in pairs(Environment) do
 		if type(v) == "table" then
@@ -2963,12 +2229,6 @@
 	end
 end
 
----Draws Sprites around the camera to provide the illusion of a flat background
----@param r number
----@param g number
----@param b number
----@param a number
----@param sprite sprite_handle? Defaults to TD's 'ui/menu/white-32.png'
 function AutoFlatBackground(r, g, b, a, sprite, distance)
 	r = AutoDefault(r, 0)
 	g = AutoDefault(g, 0)
@@ -2994,11 +2254,6 @@
 end
 end
 
----Returns and environemnt that eliminates as much lighting as possible, making colors look flat.
----
----Requires a flat DDS file.
----@param pathToDDS td_path
----@return environment
 function AutoFlatEnvironment(pathToDDS)
 	return {
 		ambient = { 1 },
@@ -3033,18 +2288,6 @@
 	}
 end
 
---#endregion
---#region Post Processing
-
----@class postprocessing
----@field saturation { [1]:any, [2]:any, [3]:any ,[4]:any }
----@field colorbalance { [1]:any, [2]:any, [3]:any ,[4]:any }
----@field brightness { [1]:any, [2]:any, [3]:any ,[4]:any }
----@field gamma { [1]:any, [2]:any, [3]:any ,[4]:any }
----@field bloom { [1]:any, [2]:any, [3]:any ,[4]:any }
-
----Returns a table of every property of the current post-processing
----@return postprocessing
 function AutoGetPostProcessing()
 	local params = {
 		'saturation',
@@ -3062,8 +2305,6 @@
 	return assembled
 end
 
----Sets every post-processing property of AutoGetPostProcessing
----@param PostProcessing postprocessing
 function AutoSetPostProcessing(PostProcessing)
 	
 	for k, v in pairs(PostProcessing) do
@@ -3077,45 +2318,18 @@
 	end
 end
 
---#endregion
---#region Debug
-
---- Returns the current Line Number.
----
---- This function is adapted from the UMF Framework
----
---- https://github.com/Thomasims/TeardownUMF/blob/master/src/util/debug.lua
----@param level integer? Optional
----@return integer
 function AutoGetCurrentLine(level)
 	level = (level or 0)
 	local _, line = pcall(error, '', level + 3) -- The level + 3 is to get out of error, then out of pcall, then out of this function
 	return tonumber(AutoSplit(line, ':')[2])
 end
 
---- Returns the current Line Number.
----
---- This function is adapted from the UMF Framework
----
---- https://github.com/Thomasims/TeardownUMF/blob/master/src/util/debug.lua
----@param level integer? Optional
----@return string?
 function AutoGetStackTrace(level)
 	level = (level or 0)
 	local _, line = pcall(error, '', level + 3) -- The level + 3 is to get out of error, then out of pcall, then out of this function
 	return line
 end
 
----Creates a neatly formatted string given any value of any type, including tables
----@param t any
----@param singleline_at number?
----@param indent_str string?
----@param round_numbers number|false?
----@param show_number_keys boolean?
----@param lua_compatible boolean?
----@param indents number?
----@param visited_tables table?
----@return string
 function AutoToString(t, singleline_at, indent_str, round_numbers, show_number_keys, lua_compatible, indents, visited_tables)
 	singleline_at = singleline_at or 1
 	indent_str = indent_str or '  '
@@ -3165,14 +2379,6 @@
 	return str
 end
 
----A Alternative to DebugPrint that uses AutoToString(), works with tables. Returns the value
----@param value any
----@param singleline_at number?
----@param indent_str string?
----@param round_numbers number|false?
----@param show_number_keys boolean?
----@param lua_compatible boolean?
----@return any
 function AutoInspect(value, singleline_at, indent_str, round_numbers, show_number_keys, lua_compatible)
 	local text = AutoToString(value, singleline_at or 3, indent_str, round_numbers, show_number_keys, lua_compatible)
 	local split = AutoSplit(text, '\n')
@@ -3187,44 +2393,20 @@
 	return value
 end
 
----AutoInspect that prints to console
----@param value any
----@param singleline_at number?
----@param indent_str string?
----@param round_numbers number|false?
----@param show_number_keys boolean?
----@param lua_compatible boolean?
----@return any
 function AutoInspectConsole(value, singleline_at, indent_str, round_numbers, show_number_keys, lua_compatible)
 	print(AutoToString(value, singleline_at or 3, indent_str, round_numbers, show_number_keys, lua_compatible))
 	return value
 end
 
----AutoInspect that prints to DebugWatch.
----
----Name will default to current line number
----@param value any
----@param name string?
----@param singleline_at number?
----@param indent_str string?
----@param round_numbers number|false?
----@param show_number_keys boolean?
----@param lua_compatible boolean?
 function AutoInspectWatch(value, name, singleline_at, indent_str, round_numbers, show_number_keys, lua_compatible)
 	if not name then name = 'Inspecting Line ' .. AutoGetCurrentLine(1) end
 	DebugWatch(name, AutoToString(value, singleline_at, indent_str, round_numbers, show_number_keys, lua_compatible))
 end
 
----Prints 24 blank lines to quote on quote, "clear the console"
 function AutoClearConsole()
 	for i = 1, 24 do DebugPrint('') end
 end
 
----Draws a Transform
----@param transform transform|vector
----@param size number? the size in meters, Default is 0.5
----@param alpha number? Default is 1
----@param draw boolean? Whether to use DebugLine or DrawLine, Default is false (DebugLine)
 function AutoDrawTransform(transform, size, alpha, draw)
 	if not transform then return end
 	if not transform['pos'] then
@@ -3258,15 +2440,6 @@
 	return transform
 end
 
----Simply draws a box given a center and the half size.
----@param point vector
----@param halfextents number|vector
----@param r number
----@param g number
----@param b number
----@param a number
----@return vector aa lower bounds point
----@return vector bb upper point
 function AutoDrawBox(point, halfextents, r, g, b, a)
 	local aa, bb = AutoAABBBoxFromPoint(point, halfextents)
 	AutoDrawAABB(aa, bb, r, g, b, a)
@@ -3274,13 +2447,6 @@
 	return aa, bb
 end
 
----Draws a Transform as a Cone
----@param transform transform
----@param sides number? the amount of sides on the cone, Default is 12
----@param angle number? how wide the cone is in degrees, Default is 25
----@param size number? the size in meters, Default is 0.5
----@param color table? Default is 1
----@param draw boolean? Whether to use DebugLine or DrawLine, Default is false (DebugLine)
 function AutoDrawCone(transform, sides, angle, size, color, draw)
 	if not transform['pos'] then
 		DebugPrint('AutoDrawCone given input not a transform')
@@ -3322,15 +2488,6 @@
 	return transform
 end
 
---#endregion
---#region Graphing
-
-AutoGraphs = {}
-
----Creates a Continuous Graph that can be drawn. The given value is added into the graph as the previous ones are kept in memory.
----@param id string
----@param value number
----@param range number? Default is 64
 function AutoGraphContinuous(id, value, range)
 	local Graph = AutoDefault(AutoGraphs[id], {
 		scan = 0,
@@ -3344,12 +2501,6 @@
 	AutoGraphs[id] = Graph
 end
 
----Creates a Graph with values within a range fed into a given function.
----@param id string
----@param rangemin number? Default is 0
----@param rangemax number? Default is 1
----@param func function? Is fed one parameter, a number ranging from rangemin to rangemax, Defaults to a Logisitc Function
----@param steps number? How many steps, or the interval of values taken from the range.
 function AutoGraphFunction(id, rangemin, rangemax, func, steps)
 	rangemin = AutoDefault(rangemin, 0)
 	rangemax = AutoDefault(rangemax, 1)
@@ -3371,13 +2522,6 @@
 	AutoGraphs[id] = Graph
 end
 
----Draws a given graph with some parameters
----@param id string
----@param sizex number width of the graph, Default is 128
----@param sizey number height of the graph, Default is 64
----@param rangemin number? If left nil, then the graph will automatically stretch the values to fill the bottom of the graph. Default is nil
----@param rangemax number? If left nil, then the graph will automatically stretch the values to fill the top of the graph. Default is nil
----@param linewidth number? The line width, Default is 2
 function AutoGraphDraw(id, sizex, sizey, rangemin, rangemax, linewidth)
 	local Graph = AutoGraphs[id]
 	if Graph == nil then error("Graph Doesn't exist, nil") end
@@ -3429,26 +2573,17 @@
 	UiPop()
 end
 
---#endregion
---#region Registry
-
----Concats any amount of strings by adding a single period between them
----@vararg string
----@return string
 function AutoKey(...)
 	return table.concat(arg, '.')
 end
 
----One out of the many methods to convert a registry key to a table
----@param key string
----@return table
 function AutoExpandRegistryKey(key)
 	local t = {}
 	local function delve(k, current)
 		local subkeys = ListKeys(k)
 		local splitkey = AutoSplit(k, '.')
 		local neatkey = splitkey[#splitkey]
-		if #subkeys > 0 then
+		if #subkeys ~= 0 then
 			current[neatkey] = {}
 			for _, subkey in ipairs(subkeys) do
 				delve(AutoKey(k, subkey), current[neatkey])
@@ -3465,137 +2600,46 @@
 	return t
 end
 
----Gets a Int from the registry, if the key does not exist, then set the key to the default value and return it.
----@param path string
----@param default integer
----@return integer
 function AutoKeyDefaultInt(path, default)
 	if path == nil then error("path nil") end
 	if HasKey(path) then
 		return GetInt(path, default)
 	else
-		SetInt(path, default)
+		SetInt(path, default, true)
 		return default
 	end
 end
 
----Gets a Float from the registry, if the key does not exist, then set the key to the default value and return it.
----@param path string
----@param default number
----@return number
 function AutoKeyDefaultFloat(path, default)
 	if path == nil then error("path nil") end
 	if HasKey(path) then
 		return GetFloat(path, default)
 	else
-		SetFloat(path, default)
+		SetFloat(path, default, true)
 		return default
 	end
 end
 
----Gets a String from the registry, if the key does not exist, then set the key to the default value and return it.
----@param path string
----@param default string
----@return string
 function AutoKeyDefaultString(path, default)
 	if path == nil then error("path nil") end
 	if HasKey(path) then
 		return GetString(path, default)
 	else
-		SetString(path, default)
+		SetString(path, default, true)
 		return default
 	end
 end
 
----Gets a Bool from the registry, if the key does not exist, then set the key to the default value and return it.
----@param path string
----@param default boolean
----@return boolean
 function AutoKeyDefaultBool(path, default)
 	if path == nil then error("path nil") end
 	if HasKey(path) then
 		return GetBool(path)
 	else
-		SetBool(path, default)
+		SetBool(path, default, true)
 		return default
 	end
 end
 
-local RegistryTableMeta = {
-	__index = function(self, key)
-		key = key:lower()
-		local path = AutoKey(rawget(self, '__path'), key)
-		if not HasKey(path) then
-			return nil
-		end
-		
-		local type = GetString(AutoKey(path, '__type'))
-		
-		if type == 'table' then
-			return AutoRegistryBindedTable(path)
-		else
-			local str = GetString(path)
-			
-			if type == 'number' then
-				return tonumber(str)
-			end
-			
-			return str
-		end
-	end,
-	__newindex = function(self, key, value)
-		key = key:lower()
-		local path = AutoKey(rawget(self, '__path'), key)
-		
-		local function dive(p, v)
-			if type(v) ~= "table" then
-				SetString(p, v)
-				
-				if type(v) ~= "nil" then
-					SetString(AutoKey(p, '__type'), type(v))
-				end
-			else
-				SetString(AutoKey(p, '__type'), 'table')
-				for k, set in pairs(v) do
-					dive(AutoKey(p, k), set)
-				end
-			end
-		end
-		
-		dive(path, value)
-	end,
-	__call = function(self)
-		local path = rawget(self, '__path')
-		
-		local function dive(p)
-			local keys = ListKeys(p)
-			local full = {}
-			
-			for i = 1, #keys do
-				local child = AutoKey(p, keys[i])
-				
-				if keys[i] ~= '__type' then
-					local t = GetString(AutoKey(child, '__type'))
-					if t == 'table' then
-						full[keys[i]] = dive(child)
-					else
-						local str = GetString(child)
-						local num = tonumber(str)
-						full[keys[i]] = num or str
-					end
-				end
-			end
-			
-			return full
-		end
-		
-		return dive(path)
-	end
-}
-
----Attempts to create a table that when written to, will update the registry, and when read from, will pull from the registry
----@param path string
----@return table
 function AutoRegistryBindedTable(path)
 	local t = {}
 	t.__path = path
@@ -3604,30 +2648,16 @@
 	return t
 end
 
---#endregion
---#region User Interface
-
----UiTranslate and UiAlign to the Center
 function AutoUiCenter()
 	UiTranslate(UiCenter(), UiMiddle())
 	UiAlign('center middle')
 end
 
----Returns the bounds, optionally subtracted by some amount
----@param subtract number?
----@return number
----@return number
 function AutoUiBounds(subtract)
 	subtract = subtract or 0
 	return UiWidth() - subtract, UiHeight() - subtract
 end
 
----Draws a line between two points in screen space
----
----Relative to current cursor position
----@param p1 { [1]:number, [2]:number }
----@param p2 { [1]:number, [2]:number }
----@param width integer? Default is 2
 function AutoUiLine(p1, p2, width)
 	width = AutoDefault(width, 2)
 	local angle = math.atan2(p2[1] - p1[1], p2[2] - p1[2]) * 180 / math.pi
@@ -3642,12 +2672,6 @@
 	UiPop()
 end
 
----Draws a cricle out of lines in screen space
----
----Relative to current cursor position
----@param radius number
----@param width integer? Default is 2
----@param steps integer?
 function AutoUiCircle(radius, width, steps)
 	width = width or 2
 	steps = steps or 16
@@ -3671,13 +2695,6 @@
 	end
 end
 
----Draws a Fancy looking Arrow between two points on the screen
----
----Relative to current cursor position
----@param p1 { [1]: number, [2]:number }
----@param p2 { [1]: number, [2]:number }
----@param line_width integer
----@param radius integer
 function AutoUIArrow(p1, p2, line_width, radius)
 	local dir = VecNormalize(VecSub(p2, p1))
 	local angle = math.atan2(unpack(AutoSwizzle(dir, 'yx')))
@@ -3687,7 +2704,7 @@
 	
 	UiPush()
 	
-	if radius > 0 then
+	if radius ~= 0 then
 		UiPush()
 		UiTranslate(unpack(p1))
 		AutoUiCircle(radius, line_width, 32)
@@ -3712,13 +2729,6 @@
 	UiPop()
 end
 
----Draws a Fancy looking Arrow between two points in the world
----
----Relative to current cursor position
----@param p1 vector
----@param p2 vector
----@param line_width integer
----@param radius integer
 function AutoUIArrowInWorld(p1, p2, line_width, radius)
 	local s_p1 = { UiWorldToPixel(p1) }
 	local s_p2 = { UiWorldToPixel(p2) }
@@ -3728,477 +2738,6 @@
 	end
 end
 
----OLD
----UI
----FUNCTIONS
-
--- AutoPad = { none = 0, atom = 4, micro = 6, thin = 12, thick = 24, heavy = 48, beefy = 128 }
-
--- AutoPrimaryColor = { 0.95, 0.95, 0.95, 1 }
--- AutoSpecialColor = { 1, 1, 0.55, 1 }
--- AutoSecondaryColor = { 0, 0, 0, 0.55 }
--- AutoFont = 'regular.ttf'
--- local SpreadStack = {}
-
--- ---Draws some text at a world position.
--- ---@param text string|number? Text Displayed, Default is 'nil'
--- ---@param position vector The WorldSpace Position
--- ---@param occlude boolean? Hides the tooltip behind walls, Default is false
--- ---@param fontsize number? Fontsize, Default is 24
--- ---@param alpha number? Alpha, Default is 0.75
--- function AutoTooltip(text, position, occlude, fontsize, alpha)
--- 	text = AutoDefault(text or "nil")
--- 	occlude = AutoDefault(occlude or false)
--- 	fontsize = AutoDefault(fontsize or 24)
--- 	alpha = AutoDefault(alpha or 0.75)
--- 	bold = AutoDefault(bold or false)
-
--- 	if occlude then if not AutoPointInView(position, nil, nil, occlude) then return end end
-
--- 	UiPush()
--- 	UiAlign('center middle')
--- 	local x, y, dist = UiWorldToPixel(position)
--- 	if dist > 0 then
--- 		UiTranslate(x, y)
--- 		UiWordWrap(UiMiddle())
-
--- 		UiFont(AutoFont, fontsize)
--- 		UiColor(0, 0, 0, 0)
--- 		local rw, rh = UiText(text)
-
--- 		UiColorFilter(1, 1, 1, alpha)
--- 		UiColor(unpack(AutoSecondaryColor))
--- 		UiRect(rw, rh)
-
--- 		UiColor(unpack(AutoPrimaryColor))
--- 		UiText(text)
--- 		UiPop()
--- 	end
--- end
-
--- ---Takes an alignment and returns a Vector representation.
--- ---@param alignment string
--- ---@return table
--- function AutoAlignmentToPos(alignment)
--- 	str, y = 0, 0
--- 	if string.find(alignment, 'left') then str = -1 end
--- 	if string.find(alignment, 'center') then str = 0 end
--- 	if string.find(alignment, 'right') then str = 1 end
--- 	if string.find(alignment, 'bottom') then y = -1 end
--- 	if string.find(alignment, 'middle') then y = 0 end
--- 	if string.find(alignment, 'top') then y = 1 end
--- 	return { x = str, y = y }
--- end
-
--- ---The next Auto Ui functions will be spread Down until AutoSpreadEnd() is called
--- ---@param padding number? The amount of padding that will be used, Default is AutoPad.thin
--- function AutoSpreadDown(padding)
--- 	table.insert(SpreadStack, { type = 'spread', direction = 'down', padding = AutoDefault(padding, AutoPad.thin) })
--- 	UiPush()
--- end
-
--- ---The next Auto Ui functions will be spread Up until AutoSpreadEnd() is called
--- ---@param padding number? The amount of padding that will be used, Default is AutoPad.thin
--- function AutoSpreadUp(padding)
--- 	table.insert(SpreadStack, { type = 'spread', direction = 'up', padding = AutoDefault(padding, AutoPad.thin) })
--- 	UiPush()
--- end
-
--- ---The next Auto Ui functions will be spread Right until AutoSpreadEnd() is called
--- ---@param padding number? The amount of padding that will be used, Default is AutoPad.thin
--- function AutoSpreadRight(padding)
--- 	table.insert(SpreadStack, { type = 'spread', direction = 'right', padding = AutoDefault(padding, AutoPad.thin) })
--- 	UiPush()
--- end
-
--- ---The next Auto Ui functions will be spread Left until AutoSpreadEnd() is called
--- ---@param padding number? The amount of padding that will be used, Default is AutoPad.thin
--- function AutoSpreadLeft(padding)
--- 	table.insert(SpreadStack, { type = 'spread', direction = 'left', padding = AutoDefault(padding, AutoPad.thin) })
--- 	UiPush()
--- end
-
--- ---The next Auto Ui functions will be spread Verticlely across the Height of the Bounds until AutoSpreadEnd() is called
--- ---@param count number? The amount of Auto Ui functions until AutoSpreadEnd()
--- function AutoSpreadVerticle(count)
--- 	table.insert(SpreadStack, { type = 'spread', direction = 'verticle', length = UiHeight(), count = count })
--- 	UiPush()
--- end
-
--- ---The next Auto Ui functions will be spread Horizontally across the Width of the Bounds until AutoSpreadEnd() is called
--- ---@param count number? The amount of Auto Ui functions until AutoSpreadEnd()
--- function AutoSpreadHorizontal(count)
--- 	table.insert(SpreadStack, { type = 'spread', direction = 'horizontal', length = UiWidth(), count = count })
--- 	UiPush()
--- end
-
--- function AutoGetSpread()
--- 	local _l = 0
--- 	local count = AutoTableCount(SpreadStack)
--- 	if count <= 0 then return nil end
--- 	for i = count, 1, -1 do
--- 		if SpreadStack[i].type == 'spread' then
--- 			_l = _l + 1
--- 			if _l >= 1 then
--- 				return SpreadStack[i], _l
--- 			end
--- 		end
--- 	end
--- 	return nil
--- end
-
--- function AutoSetSpread(Spread)
--- 	local count = AutoTableCount(SpreadStack)
--- 	for i = count, 1, -1 do
--- 		if SpreadStack[i].type == 'spread' then
--- 			str = SpreadStack[i]
--- 		end
--- 	end
-
--- 	str = Spread
--- end
-
--- ---Stop the last known Spread
--- ---@return table a table with information about the transformations used
--- function AutoSpreadEnd()
--- 	local unitdata = { comb = { w = 0, h = 0 }, max = { w = 0, h = 0 } }
--- 	-- local _, LastSpread = AutoGetSpread(1)
-
--- 	while true do
--- 		local count = #SpreadStack
-
--- 		if SpreadStack[count].type ~= 'spread' then
--- 			if SpreadStack[count].data.rect then
--- 				local rect = SpreadStack[count].data.rect
--- 				unitdata.comb.w, unitdata.comb.h = unitdata.comb.w + rect.w, unitdata.comb.h + rect.h
--- 				unitdata.max.w, unitdata.max.h = math.max(unitdata.max.w, rect.w), math.max(unitdata.max.h, rect.h)
--- 			end
-
--- 			table.remove(SpreadStack, count)
--- 		else
--- 			UiPop()
--- 			table.remove(SpreadStack, count)
-
--- 			return unitdata
--- 		end
--- 		if count <= 0 then
--- 			return unitdata
--- 		end
--- 	end
--- end
-
--- function AutoHandleSpread(gs, data, type, spreadpad)
--- 	spreadpad = AutoDefault(spreadpad, false)
-
--- 	if not AutoGetSpread() then return end
-
--- 	if gs ~= nil then
--- 		if not spreadpad then pad = 0 else pad = gs.padding end
--- 		if gs.direction == 'down' then
--- 			UiTranslate(0, data.rect.h + pad)
--- 		elseif gs.direction == 'up' then
--- 			UiTranslate(0, -(data.rect.h + pad))
--- 		elseif gs.direction == 'right' then
--- 			UiTranslate(data.rect.w + pad, 0)
--- 		elseif gs.direction == 'left' then
--- 			UiTranslate(-(data.rect.w + pad), 0)
--- 		elseif gs.direction == 'verticle' then
--- 			UiTranslate(0, gs.length / gs.count * 1.5 + gs.length / gs.count)
--- 		elseif gs.direction == 'horizontal' then
--- 			UiTranslate(gs.length / gs.count, 0)
--- 		end
--- 	end
-
--- 	if type ~= nil then
--- 		table.insert(SpreadStack, { type = type, data = data })
--- 	end
--- end
-
--- ---Given the current string, will return a modified string based on the input of the user. It's basically just a text box. Has a few options.
--- ---@param current any
--- ---@param maxlength any
--- ---@param allowlowercase any
--- ---@param allowspecial any
--- ---@param forcekey any
--- ---@return any
--- ---@return any
--- ---@return boolean
--- function AutoTextInput(current, maxlength, allowlowercase, allowspecial, forcekey)
--- 	current = AutoDefault(current, '')
--- 	maxlength = AutoDefault(maxlength, 1 / 0)
--- 	allowlowercase = AutoDefault(allowlowercase, true)
--- 	allowspecial = AutoDefault(allowspecial, true)
--- 	forcekey = AutoDefault(forcekey, nil)
-
--- 	local modified = current
-
--- 	local special = {
--- 		['1'] = '!',
--- 		['2'] = '@',
--- 		['3'] = '#',
--- 		['4'] = '$',
--- 		['5'] = '%',
--- 		['6'] = '^',
--- 		['7'] = '&',
--- 		['8'] = '*',
--- 		['9'] = '(',
--- 		['0'] = ')',
--- 	}
--- 	local lpk = forcekey or InputLastPressedKey()
-
--- 	if lpk == 'backspace' then
--- 		modified = modified:sub(1, #modified - 1)
--- 	elseif lpk == 'delete' then
--- 		modified = ''
--- 	elseif #modified < maxlength then
--- 		if lpk == 'space' then
--- 			modified = modified .. ' '
--- 		elseif #lpk == 1 then
--- 			if not InputDown('shift') then
--- 				if allowlowercase then
--- 					lpk = lpk:lower()
--- 				end
--- 			else
--- 				if allowspecial and special[lpk] then
--- 					lpk = special[lpk]
--- 				end
--- 			end
-
--- 			modified = modified .. lpk
--- 		end
--- 	end
-
--- 	return modified, lpk ~= '' and lpk or nil, modified ~= current
--- end
-
--- -- local keys = {
--- -- 	"lmb", "mmb", "rmb", -- mouse
--- -- 	"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", -- numerical
--- -- 	"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
--- -- 	"y", "z", -- alphabatical
--- -- 	"f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", -- function key
--- -- 	"uparrow", "downarrow", "leftarrow", "rightarrow", -- arrow key
--- -- 	"backspace", "alt", "delete", "home", "end", "pgup", "pgdown", "insert", "return", "space", "shift", "ctrl", "tab",
--- -- 	"esc", --random key
--- -- 	",", ".", "-", "+", -- undocumented key (yes, '=' key is '+' key)
--- -- }
-
--- -------------------------------------------------------------------------------------------------------------------------------------------------------
--- ----------------User Interface Creation Functions------------------------------------------------------------------------------------------------------
--- -------------------------------------------------------------------------------------------------------------------------------------------------------
-
--- ---Create a Container with new bounds
--- ---@param width number
--- ---@param height number
--- ---@param padding number? The Amount of padding against sides of the container, Default is AutoPad.micro
--- ---@param clip boolean? Whether  to clip stuff outside of the container, Default is false
--- ---@param draw boolean? Draws the container's background, otherwise it will be invisible, Default is true
--- ---@return table containerdata
--- function AutoContainer(width, height, padding, clip, draw)
--- 	width = AutoDefault(width, 300)
--- 	height = AutoDefault(height, 400)
--- 	padding = math.max(AutoDefault(padding, AutoPad.micro), 0)
--- 	clip = AutoDefault(clip, false)
--- 	draw = AutoDefault(draw, true)
-
--- 	local paddingwidth = math.max(width - padding * 2, padding * 2)
--- 	local paddingheight = math.max(height - padding * 2, padding * 2)
-
--- 	UiWindow(width, height, clip)
-
--- 	UiAlign('left top')
--- 	if draw then
--- 		UiPush()
--- 		UiColor(unpack(AutoSecondaryColor))
--- 		UiImageBox("ui/common/box-solid-10.png", UiWidth(), UiHeight(), 10, 10)
--- 		UiPop()
--- 	end
-
--- 	hover = UiIsMouseInRect(UiWidth(), UiHeight())
-
--- 	UiTranslate(padding, padding)
--- 	UiWindow(paddingwidth, paddingheight, false)
-
--- 	local offset = { x = 0, y = 0 }
-
--- 	UiTranslate(offset.x, offset.y)
-
--- 	return { rect = { w = paddingwidth, h = paddingheight }, hover = hover }
--- end
-
--- ---Creates a Button
--- ---@param name string
--- ---@param fontsize number
--- ---@param paddingwidth number Amount of padding used Horizontally
--- ---@param paddingheight number Amount of padding used Vertically
--- ---@param draw boolean Draws the Button
--- ---@param spreadpad boolean Adds padding when used with AutoSpread...()
--- ---@return boolean Pressed
--- ---@return table ButtonData
--- function AutoButton(name, fontsize, color, paddingwidth, paddingheight, draw, spreadpad)
--- 	fontsize = AutoDefault(fontsize, 28)
--- 	color = AutoDefault(color, AutoPrimaryColor)
--- 	paddingwidth = AutoDefault(paddingwidth, AutoPad.thick)
--- 	paddingheight = AutoDefault(paddingheight, AutoPad.thin)
--- 	draw = AutoDefault(draw, true)
--- 	spreadpad = AutoDefault(spreadpad, true)
-
--- 	UiPush()
--- 	UiWordWrap(UiWidth() - AutoPad.thick)
--- 	UiFont(AutoFont, fontsize)
--- 	UiButtonHoverColor(unpack(AutoSpecialColor))
--- 	UiButtonPressColor(0.75, 0.75, 0.75, 1)
--- 	UiButtonPressDist(0.25)
-
--- 	UiColor(0, 0, 0, 0)
--- 	local rw, rh = UiText(name)
--- 	local padrw, padrh = rw + paddingwidth * 2, rh + paddingheight * 2
-
--- 	if draw then
--- 		hover = UiIsMouseInRect(padrw, padrh)
--- 		UiColor(unpack(color))
-
--- 		UiButtonImageBox('ui/common/box-outline-6.png', 6, 6, unpack(color))
--- 		pressed = UiTextButton(name, padrw, padrh)
--- 	end
--- 	UiPop()
-
--- 	local data = { pressed = pressed, hover = hover, rect = { w = padrw, h = padrh } }
--- 	if draw then AutoHandleSpread(AutoGetSpread(), data, 'draw', spreadpad) end
-
--- 	return pressed, data
--- end
-
--- ---Draws some Text
--- ---@param name string
--- ---@param fontsize number
--- ---@param draw boolean Draws the Text
--- ---@param spread boolean Adds padding when used with AutoSpread...()
--- ---@return table TextData
--- function AutoText(name, fontsize, color, draw, spread)
--- 	fontsize = AutoDefault(fontsize, 28)
--- 	draw = AutoDefault(draw, true)
--- 	spread = AutoDefault(spread, true)
-
--- 	UiPush()
--- 	UiWordWrap(UiWidth() - AutoPad.thick)
--- 	UiFont(AutoFont, fontsize)
-
--- 	UiColor(0, 0, 0, 0)
--- 	local rw, rh = UiText(name)
-
--- 	if draw then
--- 		UiPush()
--- 		UiWindow(rw, rh)
--- 		AutoCenter()
-
--- 		UiColor(unpack(color or AutoPrimaryColor))
--- 		UiText(name)
--- 		UiPop()
--- 	end
--- 	UiPop()
-
--- 	local data = { rect = { w = rw, h = rh }, hover = UiIsMouseInRect(rw, rh) }
--- 	if spread then AutoHandleSpread(AutoGetSpread(), data, 'draw', true) end
-
--- 	return data
--- end
-
--- ---Creates a Slider
--- ---@param set number The Current Value
--- ---@param min number The Minimum
--- ---@param max number The Maximum
--- ---@param lockincrement number The increment
--- ---@param paddingwidth Amount of padding used Horizontally
--- ---@param paddingheight Amount of padding used Vertically
--- ---@param spreadpad boolean Adds padding when used with AutoSpread...()
--- ---@return number NewValue
--- ---@return table SliderData
--- function AutoSlider(set, min, max, lockincrement, paddingwidth, paddingheight, spreadpad)
--- 	min = AutoDefault(min, 0)
--- 	max = AutoDefault(max, 1)
--- 	set = AutoDefault(set, min)
--- 	lockincrement = AutoDefault(lockincrement, 0)
--- 	paddingwidth = AutoDefault(paddingwidth, AutoPad.thick)
--- 	paddingheight = AutoDefault(paddingheight, AutoPad.micro)
--- 	spreadpad = AutoDefault(spreadpad, true)
-
--- 	local width = UiWidth() - paddingwidth * 2
--- 	local dotwidth, dotheight = UiGetImageSize("MOD/slider.png")
-
--- 	local screen = AutoMap(set, min, max, 0, width)
-
--- 	UiPush()
--- 	UiTranslate(paddingwidth, paddingheight)
--- 	UiColor(unpack(AutoSpecialColor))
-
--- 	UiPush()
--- 	UiTranslate(0, dotheight / 2)
--- 	UiRect(width, 2)
--- 	UiPop()
-
--- 	UiTranslate(-dotwidth / 2, 0)
-
--- 	screen, released = UiSlider('MOD/slider.png', "x", screen, 0, width)
--- 	screen = AutoMap(screen, 0, width, min, max)
--- 	screen = AutoRound(screen, lockincrement)
--- 	screen = AutoClamp(screen, min, max)
--- 	set = screen
--- 	UiPop()
-
--- 	local data = { value = set, released = released, rect = { w = width, h = paddingheight * 2 + dotheight } }
--- 	AutoHandleSpread(AutoGetSpread(), data, 'draw', spreadpad)
-
--- 	return set, data
--- end
-
--- ---Draws an Image
--- ---@param path string
--- ---@param width number
--- ---@param height number
--- ---@param alpha number
--- ---@param draw boolean Draws the Image
--- ---@param spreadpad boolean Adds padding when used with AutoSpread...()
--- ---@return table ImageData
--- function AutoImage(path, width, height, border, spreadpad)
--- 	local w, h = UiGetImageSize(path)
--- 	width = AutoDefault(width, (height == nil and UiWidth() or (height * (w / h))))
--- 	height = AutoDefault(height, width * (h / w))
--- 	border = AutoDefault(border, 0)
--- 	draw = AutoDefault(draw, true)
--- 	spreadpad = AutoDefault(spreadpad, true)
-
--- 	UiPush()
--- 	UiImageBox(path, width, height, border, border)
--- 	UiPop()
-
--- 	local hover = UiIsMouseInRect(width, height)
-
--- 	local data = { hover = hover, rect = { w = width, h = height } }
--- 	if draw then AutoHandleSpread(AutoGetSpread(), data, 'draw', spreadpad) end
-
--- 	return data
--- end
-
--- ---Creates a handy little marker, doesnt effect anything, purely visual
--- ---@param size number, Default is 1
--- function AutoMarker(size)
--- 	size = AutoDefault(size, 1) / 2
--- 	UiPush()
--- 	UiAlign('center middle')
--- 	UiScale(size, size)
--- 	UiColor(unpack(AutoSpecialColor))
--- 	UiImage('ui/common/dot.png')
--- 	UiPop()
--- end
-
---#endregion
---#region Cursed
-
----Loads a string as `return <lua_string>`
----@param lua_string string
----@return boolean success
----@return unknown? return_value
 function AutoParse(lua_string)
 	local formatted = 'return ' .. lua_string
 	local success, func = pcall(loadstring, formatted)
@@ -4212,21 +2751,13 @@
 	return false
 end
 
----A very sinful way to pipe raw code into the registry, use in combination with `AutoCMD_Parse`
----@param path string
----@param luastr string
 function AutoCMD_Pipe(path, luastr)
 	local keys = ListKeys(path)
 	local newkey = AutoKey(path, #keys + 1)
 	
-	SetString(newkey, luastr)
-end
-
----A very sinful way to parse raw code from the registry, use in combination with `AutoCMD_Pipe`
----
----_God is dead and we killed her._
----@param path string
----@return table<{ cmd:string, result:any }>
+	SetString(newkey, luastr, true)
+end
+
 function AutoCMD_Parse(path)
 	local results = {}
 	for index = 1, #ListKeys(path) do
@@ -4247,4 +2778,3 @@
 	return results
 end
 
---#endregion
```

---

# Migration Report: script\CONFIG.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\CONFIG.lua
+++ patched/script\CONFIG.lua
@@ -1,31 +1 @@
---[[
-#include "loadpatch.lua"
-]]
-
-zombie_mod_id = Loader.mod_id
--- zombie_mod_id = 'local-zombies--autumnatic-'
--- zombie_mod_id = 'steam-3011292197' -- PUBLIC RELEASE
--- zombie_mod_id = 'steam-3013598090' -- EXPERIMENTAL RELEASE
-
-zombie_root = GetString(('mods.available.%s.path'):format(zombie_mod_id))
-
-zombie_scheme = 'AutumnZombie' -- This gets added as a tag to all bodies and shapes of the zombie, the purpose of this is for compatability, if you want to say that your mod is not compatable with other mods meant to effect the zombies, then change this. If you want to have a custom Zglobal.lua script, then change this.
-zombie_global_key = AutoKey('level', zombie_scheme)
-zombie_lua_pipe = AutoKey(zombie_global_key, 'lua')
-zombie_blood_key = AutoKey(zombie_global_key, 'blood')
-zombie_handle_cleanup = AutoKey(zombie_global_key, 'cleanup')
-zombie_add_blood_indicies = AutoKey(zombie_global_key, 'addbloodindicies')
-
-zombie_shape_layer = 2
-zombie_arm_shape_layer = 4
-
-zombie_blood_shape_tag = AutoKey(zombie_scheme, 'BloodIndicies')
-
-if CreateMaterial then
-	zombie_blood_materials = {
-		CreateMaterial(nil, AutoColors.red_light[1], AutoColors.red_light[2], AutoColors.red_light[3], 1, 0, 1, 0.6),
-		CreateMaterial(nil, AutoColors.red_dark[1], AutoColors.red_dark[2], AutoColors.red_dark[3], 1, 0, 1, 0.6),
-		CreateMaterial(nil, AutoColors.background_light[1], AutoColors.background_light[2], AutoColors.background_light[3], 1, 0, 1, 0.6),
-		CreateMaterial(nil, AutoColors.background_dark[1], AutoColors.background_dark[2], AutoColors.background_dark[3], 1, 0, 1, 0.6),
-	}
-end+#version 2

```

---

# Migration Report: script\loadpatch.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\loadpatch.lua
+++ patched/script\loadpatch.lua
@@ -1,21 +1,4 @@
---- Had to copy paste some code for latest update compatibility - fuck you, make your own mods if you think its messy.
----
---- For any dev reading this: lol im so sorry,
---- I assure you that this is the messiest code I've ever written,
---- understand that when this mod was created, this was the only known
---- way to go about doing things like this, and a majority of the tech
---- here I had to learn from experimentation, as the dev-help and documentation
---- is abysmal at best, and out-right incorrect at worst.
----
---- I drew blood from the concrete to make this mod so if the
---- lamb that you care for is disfigured than so be it.
----
---- Below is some is part of a better solution that I had to mesh with the old method.
-
-Loader = {}
-
----Leave blank to find itself.
----@param set_mod_id string?
+#version 2
 function Loader.Set(set_mod_id)
     if set_mod_id then
         Loader.mod_id = set_mod_id
@@ -75,4 +58,3 @@
     end
 end
 
-Loader.Set()

```

---

# Migration Report: script\pal.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\pal.lua
+++ patched/script\pal.lua
@@ -1,23 +1,7 @@
---[[
-#include shape_utils.lua
-]]
-
+#version 2
 local all_materials = { "foliage", "dirt", "plaster", "plastic", "glass", "wood", "masonry", "hardmasonry", "metal", "heavymetal", "hardmetal", "rock", "ice", "unphysical" }
 local unbreakable_materials = { 'none', 'hardmasonry', 'heavymetal', 'hardmetal', 'rock', }
 
----@class materialEntry: { material:material, r:number, g:number, b:number, a:number, reflect:number, shiny:number, metal:number, emissive:number }
-
----Simple wrapper for creating material entries for palettes.
----@param material material?
----@param r number?
----@param g number?
----@param b number?
----@param a number?
----@param reflect number?
----@param shiny number?
----@param metal number?
----@param emissive number?
----@return materialEntry
 function CreateMaterial(material, r, g, b, a, reflect, shiny, metal, emissive)
     return {
         material = material or 'none',
@@ -32,9 +16,6 @@
     }
 end
 
----Merges two material togther, if any values are missing from Newest, take from Oldest
----@param Newest materialEntry
----@param Oldest materialEntry
 function MergeMaterials(Newest, Oldest)
     Oldest = Oldest or CreateMaterial()
 	for k in pairs(Oldest) do
@@ -42,19 +23,10 @@
 	end
 end
 
----`pairs` but for all the materials minus "none"
----@return fun(table: table<number, material>, index?: number):number, material
 function pairsMaterials()
     return pairs(all_materials)
 end
 
----Adds `materials` into any avaliable space within the given palette.
----Can set custom ranges for padding.
----@param palette materialEntry[]
----@param materials materialEntry[]
----@param color_range { [1]:number, [2]:number }? Default is `{2, 222}` - *Gives some padding for engine colors and defaults in first index*
----@param priority material|material[]|'unbreakable'
----@return integer[] newly_created_indexes
 function AddMaterialsToPalette(palette, materials, color_range, priority)
     color_range = color_range or { 2, 222 }
     local prio_table = priority and ((type(priority) == 'table') and (priority) or (priority == 'unbreakable' and (unbreakable_materials) or { priority })) or {}
@@ -109,4 +81,5 @@
     end
 
     return indexes
-end+end
+

```

---

# Migration Report: script\shape_utils.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\shape_utils.lua
+++ patched/script\shape_utils.lua
@@ -1,261 +1,3 @@
--- TODO: doc
-
--- This should be the mod path to THIS FILE
+#version 2
 local FILENAME = "MOD/script/shape_utils.lua"
 
-if ClearKey then -- <script>
-	local function voxscript( parameters )
-		local size = ""
-		local shapedata = ""
-		local palettedata = ""
-		if parameters.palette then
-			local palette = {}
-			for i = 1, #parameters.palette do
-				local p = parameters.palette[i]
-				palette[i] = string.format( "%d/%s/%d/%d/%d/%f/%f/%f/%f/%f", p.index, p.material or "none", math.floor( p.r * 255 ),
-				                            math.floor( p.g * 255 ), math.floor( p.b * 255 ),
-				                            p.a and p.a > 0 and p.a < 1 and 0.5 or 1, p.reflect, p.shiny, p.metal, p.emissive )
-			end
-			palettedata = string.format( "palette=\"%s\"", table.concat( palette, " " ) )
-		end
-		if parameters.shape then
-			local content = {}
-			for i = 1, #parameters.shape do
-				local index = parameters.shape[i]
-				content[i] = string.char( math.floor( index / 16 ) + 65, index % 16 + 65 )
-			end
-			shapedata = string.format( "shape=\"%s\"", table.concat( content, "" ) )
-		end
-		if parameters.size then
-			size = string.format( "size=\"%d %d %d\"", unpack( parameters.size ) )
-		end
-		return string.format( "<voxscript file=\"%s\"><parameters %s %s %s/></voxscript>", FILENAME, size, shapedata,
-		                      palettedata )
-	end
-
-	function CreatePalette( entries )
-		local palettexml = voxscript { palette = entries }
-		return Spawn( palettexml, Transform(), true, false )[1]
-	end
-
-	function SetShapePaletteContent( shape, entries )
-		local palette = CreatePalette( entries )
-		CopyShapePalette( palette, shape )
-		Delete( palette )
-	end
-
-	function SetShapesPaletteContent( shapes, entries )
-		local palette = CreatePalette( entries )
-		for i = 1, #shapes do
-			CopyShapePalette( palette, shapes[i] )
-		end
-		Delete( palette )
-	end
-
-	function GetShapePaletteContent( shape )
-		local forward = GetShapePalette( shape )
-		local reverse = {}
-		for i = 1, #forward do
-			local mat, r, g, b, a, re, sh, me, em = GetShapeMaterial( shape, forward[i] )
-			local t = {
-				index = forward[i],
-				material = mat,
-				r = r,
-				g = g,
-				b = b,
-				a = a,
-				reflect = re,
-				shiny = sh,
-				metal = me,
-				emissive = em,
-			}
-			forward[i] = t
-			reverse[t.index] = t
-		end
-		return forward, reverse
-	end
-
-	function GetShapesPaletteContent( shapes )
-		local forward = {}
-		local reverse = {}
-		for i = 1, #shapes do
-			local shape = shapes[i]
-			local usedpalette = GetShapePalette( shape )
-			for j = 1, #usedpalette do
-				if not reverse[usedpalette[j]] then
-					local material, r, g, b, a, re, sh, me, em = GetShapeMaterial( shape, usedpalette[j] )
-					local t = {
-						index = usedpalette[j],
-						material = material,
-						r = r,
-						g = g,
-						b = b,
-						a = a,
-						reflect = re,
-						shiny = sh,
-						metal = me,
-						emissive = em,
-					}
-					forward[#forward + 1] = t
-					reverse[usedpalette[j]] = t
-				end
-			end
-		end
-		return forward, reverse
-	end
-
-	function CreateShapeFromContent( content, x2, y2, z2 )
-		if not x2 then
-			content, x2, y2, z2 = unpack( content )
-		end
-		local newdataxml = voxscript { shape = content, size = { x2, y2, z2 } }
-		local newdata = Spawn( newdataxml, Transform(), true, false )[1]
-		SetBrush( "cube", 1, content[1] )
-		DrawShapeBox( newdata, 0, 0, 0, 0, 0, 0 )
-		SetBrush( "cube", 1, content[#content] )
-		DrawShapeBox( newdata, x2 - 1, y2 - 1, z2 - 1, x2 - 1, y2 - 1, z2 - 1 )
-		return newdata
-	end
-
-	function SetShapeContent( shape, content )
-		local x2, y2, z2 = GetShapeSize( shape )
-		if type( content[1] ) == "table" then
-			content, x2, y2, z2 = unpack( content )
-		end
-		local newdata = CreateShapeFromContent( content, x2, y2, z2 )
-		CopyShapeContent( newdata, shape )
-		Delete( newdata )
-	end
-
-	function GetShapeContent( shape )
-		local content = {}
-		local x2, y2, z2 = GetShapeSize( shape )
-		for x = 0, x2 - 1 do
-			for y = 0, y2 - 1 do
-				for z = 0, z2 - 1 do
-					local _, _, _, _, _, index = GetShapeMaterialAtIndex( shape, x, y, z )
-					content[#content + 1] = index
-				end
-			end
-		end
-		return content, x2, y2, z2
-	end
-
-	function CarveShape( shape, carver, offset )
-		-- TODO: batch carving?
-		if type( carver ) == "number" then
-			carver = { GetShapeContent( carver ), GetShapeSize( carver ) }
-		end
-		local oP, oR = Vec( 0, 0, 0 ), Vec( 0, 0, 0 )
-		if offset then
-			if offset.pos then
-				oP = offset.pos
-				oR = Vec( GetQuatEuler( offset.rot ) )
-			else
-				oP = offset
-			end
-		end
-		local original = GetShapeContent( shape )
-		local positive = voxscript { shape = original, size = { GetShapeSize( shape ) } }
-		local negative = type( carver ) == "string" and string.format( [[<vox file="%s"/>]], carver ) or
-			                 voxscript { shape = carver[1], size = { select( 2, unpack( carver ) ) } }
-		local xml = string.format( [[
-			<body dynamic="true">
-				%s
-				<group pos="%f %f %f" rot="%f %f %f">
-					%s
-				</group>
-			</body>
-		]], positive, oP[1], oP[2], oP[3], oR[1], oR[2], oR[3], negative )
-		local body, resultShape, negativeShape = unpack( Spawn( xml, Transform(), false, false ) )
-		CopyShapeContent( resultShape, shape )
-		SetShapeLocalTransform( shape, TransformToParentTransform( GetShapeLocalTransform( shape ),
-		                                                           GetShapeWorldTransform( resultShape ) ) )
-		Delete( body )
-		Delete( resultShape )
-		Delete( negativeShape )
-		return shape
-	end
-
-	function CloneShape( shape )
-		local save = CreateShape()
-		CopyShapeContent( shape, save )
-		local x, y, z, scale = GetShapeSize( shape )
-		local start = GetShapeWorldTransform( shape )
-		ResizeShape( shape, 0, 0, 0, x - 1, y - 1, z + 1 )
-		SetBrush( "cube", 1, 1 )
-		DrawShapeBox( shape, 0, 0, z + 1, 0, 0, z + 1 )
-		local pieces = SplitShape( shape, false )
-		local moved = VecScale( TransformToLocalPoint( GetShapeWorldTransform( shape ), start.pos ), 1 / scale )
-		local mx, my, mz = math.floor( moved[1] + 0.5 ), math.floor( moved[2] + 0.5 ), math.floor( moved[3] + 0.5 )
-		ResizeShape( shape, mx, my, mz, 1, 1, 1 )
-		CopyShapeContent( save, shape )
-		local splitoffset = VecScale( TransformToLocalPoint( GetShapeWorldTransform( pieces[1] ), start.pos ), 1 / scale )
-		local sx, sy, sz = math.floor( splitoffset[1] + 0.5 ), math.floor( splitoffset[2] + 0.5 ),
-							math.floor( splitoffset[3] + 0.5 )
-		ResizeShape( pieces[1], sx, sy, sz, 1, 1, 1 )
-		CopyShapeContent( save, pieces[1] )
-		Delete( save )
-		for i = 2, #pieces do
-			Delete( pieces[i] )
-		end
-		return pieces[1], shape
-	end
-else -- <voxscript>
-	local sx, sy, sz = GetInt( "size", 1, 1, 1 )
-	local shapedata = GetString( "shape" )
-	local palettedata = GetString( "palette" )
-
-	local function getbyte( str, offset )
-		local a, b = string.byte( str, offset, offset + 1 )
-		return (a - 65) * 16 + b - 65
-	end
-
-	function init()
-		if palettedata and palettedata ~= "" then
-			local colors = {}
-			for index, m, r, g, b, a, re, sh, me, em in palettedata:gmatch(
-				                                            "(%d+)/(%w+)/(%d+)/(%d+)/(%d+)/([%d.]+)/([%d.]+)/([%d.]+)/([%d.]+)/([%d.]+)" ) do
-				colors[tonumber( index )] = {
-					m,
-					tonumber( r ) / 255,
-					tonumber( g ) / 255,
-					tonumber( b ) / 255,
-					tonumber( a ),
-					tonumber( re ),
-					tonumber( sh ),
-					tonumber( me ),
-					tonumber( em ),
-				}
-			end
-			for i = 1, 255 do
-				if colors[i] then
-					CreateMaterial( unpack( colors[i] ) )
-				else
-					CreateMaterial( "none" ) -- gaps in the palette can't be left out
-				end
-			end
-			if not shapedata or shapedata == "" then
-				Vox( 0, 0, 0, 0, 0, 0 )
-				for index in pairs( colors ) do
-					Material( index )
-					Box( index - 1, 0, 0, index, 1, 1 )
-				end
-			end
-		end
-		if shapedata and shapedata ~= "" then
-			Vox( 0, 0, 0, 0, 0, 0 )
-			for i = 0, #shapedata / 2 - 1 do
-				local index = getbyte( shapedata, i * 2 + 1 )
-				if index > 0 then
-					Material( index )
-					local x, y, z = math.floor( i / sy / sz ) % sx, math.floor( i / sz ) % sy, i % sz
-					Box( x, y, z, x + 1, y + 1, z + 1 )
-				end
-			end
-			Material( 1 ) -- ensure the shape size is as requested
-			Box( 0, 0, 0, 1, 1, 1 )
-			Box( sx - 1, sy - 1, sz - 1, sx, sy, sz )
-		end
-	end
-end
```

---

# Migration Report: script\Zcmd\apply_tag.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zcmd\apply_tag.lua
+++ patched/script\Zcmd\apply_tag.lua
@@ -1,10 +1,5 @@
---[[
-#include ../Automatic.lua
-#include ../CONFIG.lua
-#include ../Zhelper.lua
-]]
-
-function init()
+#version 2
+function server.init()
     local z = {}
     for _, b in pairs(FindBodies(zombie_scheme, true)) do
         local script_handle = tonumber(GetTagValue(b, zombie_scheme))
@@ -12,13 +7,11 @@
             z[script_handle] = true
         end
     end
-
     local tag = GetStringParam('tag')
     local value = GetStringParam('value')
-
     for handle in pairs(z) do
         SetTag(handle, tag, value)
     end
+    SignScriptUpForRemoval(AutoGetScriptHandle())
+end
 
-    SignScriptUpForRemoval(AutoGetScriptHandle())
-end
```

---

# Migration Report: script\Zcmd\cleanup.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zcmd\cleanup.lua
+++ patched/script\Zcmd\cleanup.lua
@@ -1,12 +1,13 @@
---[[
-#include ../Automatic.lua
-#include ../CONFIG.lua
-#include ../Zhelper.lua
-]]
+#version 2
+function server.init()
+    local z = {}
+    for handle in pairs(z) do
+        Delete(handle)
+    end
+    SignScriptUpForRemoval(AutoGetScriptHandle())
+end
 
-function init()
-    local z = {}
-
+function client.init()
     ParticleReset()
     ParticleType("plain")
     ParticleRadius(0.05, 0.05)
@@ -16,17 +17,16 @@
     ParticleDrag(0.1)
     ParticleAlpha(1, 1, "easein")
     ParticleSticky(0, 0.5)
-    
     for _, b in pairs(FindBodies(zombie_scheme, true)) do
         z[tonumber(GetTagValue(b, zombie_scheme))] = true
-        
+
         for _, s in pairs(GetBodyShapes(b)) do
             local obb = AutoGetShapeOBB(s)
-            
+
             for i=1, 16 do
                 local vec = AutoVecMulti(AutoVecRnd(math.random()), obb.size)
                 local p = TransformToParentPoint(obb, vec)
-                
+
                 local cs = math.random() > 0.5 and AutoColors.red_light or AutoColors.red_dark
                 local ce = math.random() > 0.5 and AutoColors.red_light or AutoColors.red_dark
                 ParticleColor(cs[1], cs[2], cs[3], ce[1], ce[2], ce[3])
@@ -38,10 +38,5 @@
 
         Delete(b)
     end
+end
 
-    for handle in pairs(z) do
-        Delete(handle)
-    end
-
-    SignScriptUpForRemoval(AutoGetScriptHandle())
-end
```

---

# Migration Report: script\Zcmd\king of the hill.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zcmd\king of the hill.lua
+++ patched/script\Zcmd\king of the hill.lua
@@ -1,198 +1,6 @@
---[[
-#include ../Automatic.lua
-#include ../pal.lua
-#include ../CONFIG.lua
-#include ../Zhelper.lua
-]]
-
----@class tile
----@field prev string|false
----@field node node
----@field hue number
----@field distance number
-
----@class node
----@field prev node|false
----@field pos_str string
----@field connections node[]
----@field covered string[]
----@field hue number
-
-function init()
-    ORIGIN = Vec()
-    MAP = {
-        Tile_Size = 0.6,
-        ---@type tile[]
-        Explored_Tiles = {},
-        ---@type tile[]
-        Unexplored_Tiles = {},
-        ---@type tile[]
-        Ground_Tiles = {},
-        ---@type tile[]
-        Wall_Tiles = {},
-        ---@type tile[]
-        Edge_Tiles = {},
-    }
-
-
-    Last_Zombie_Spawn_Time = -1/0
-    ZOMBIES = {}
-
-    ---@type node
-    ---@diagnostic disable-next-line
-    NETWORK = false
-
-    DEBUG = {
-        network = false,
-        map = false,
-        queries = true,
-    }
-
-    NEIGHBOR = {
-        ortho_horizontal =      { Vec(-1, 0, 0), Vec(1, 0, 0), Vec(0, 0, -1), Vec(0, 0, 1), },
-        all_horizontal =        { Vec(-1, 0, 0), Vec(1, 0, 0), Vec(0, 0, -1), Vec(0, 0, 1), Vec(-1, 0, -1), Vec(1, 0, -1), Vec(-1, 0, -1), Vec(-1, 0, 1), },
-        up_middle_down =        { down = Vec(0, -1), up = Vec(0, 1), middle = Vec() },
-    }
-
-    SPAWN_PATH = AutoSplit(GetStringParam('spawn', 'MOD/xml/default.xml'), ',')
-    Interval = GetFloatParam('interval', 2)
-    NOPATH = GetBoolParam('nopath', false)
-    QUERY_REQUIREMENTS = 'physical large'
-    SAFE_DISTANCE = 5
-    SCRIPT_HANDLE = AutoGetScriptHandle()
-
-    C_Explore = coroutine.create(Explore)
-    -- C_Draw = coroutine.wrap(function ()
-    --     while true do
-            -- DrawTiles(MAP.Explored_Tiles)
-    --         coroutine.yield()
-    --         DrawTiles(MAP.Unexplored_Tiles)
-    --         coroutine.yield()
-    --     end
-    -- end)
-end
-
+#version 2
 function handleCommand(cmd)
     if cmd == 'quickload' then init() end
-end
-
-function tick(dt)
-    if GetString('game.player.tool') == 'none' then
-        ORIGIN = AutoRaycast(AutoRaycastCamera(true, 150, 0, true).intersection, Vec(0, -1), 128, 0.1).intersection
-
-        ParticleLine(VecAdd(ORIGIN, Vec(math.cos(GetTime() * 22) * 0.25, 1, math.sin(GetTime() * 22) * 0.25)), ORIGIN, GetTime() / 3, GetTime() / 3, 2)
-
-        if not InputDown('shift') then
-            SAFE_DISTANCE = AutoClamp(SAFE_DISTANCE + InputValue('mousewheel'), 1, 20)
-        end
-
-        local v1 = Vec(SAFE_DISTANCE, 0, 0)
-        for t = 0, math.pi * 2, math.pi / 32 do
-            local v2 = Vec(math.cos(t) * SAFE_DISTANCE, 0, math.sin(t) * SAFE_DISTANCE)
-            DrawLine(VecAdd(ORIGIN, v1), VecAdd(ORIGIN, v2))
-            DrawLine(VecAdd(ORIGIN, v1), ORIGIN)
-            v1 = VecCopy(v2)
-        end
-
-        SetBool('game.disablepause', true)
-        if InputPressed('esc') then
-            SignScriptUpForRemoval(SCRIPT_HANDLE)
-        end
-    else
-        -- if InputPressed('y') then
-        --     SignUpForRemoval(SCRIPT_HANDLE)
-        -- end
-
-        -- if InputPressed('u') then
-        --     DEBUG.network = not DEBUG.network
-        -- end
-
-        -- if InputPressed('i') then
-        --     DEBUG.map = not DEBUG.map
-        -- end
-
-        if AutoPrimaryMenuButton('Kill Spawner') then
-            SignScriptUpForRemoval(SCRIPT_HANDLE)
-        end
-
-        if C_Explore then
-            if coroutine.status(C_Explore) == "suspended" then coroutine.resume(C_Explore) end
-
-            SetBool('game.disablepause', true)
-            if InputPressed('esc') or coroutine.status(C_Explore) == "dead" then
-                C_Explore = nil
-            end
-        else
-            if GetTime() - Last_Zombie_Spawn_Time > Interval then
-                for i, script in pairs(ZOMBIES) do
-                    if GetTagValue(script, 'status') ~= 'alive' then
-                        table.remove(ZOMBIES, i)
-                    end
-                end
-                    
-                if #ZOMBIES < 15 then
-                    local l = {}
-            
-                    for pos_str, data in pairs(MAP.Explored_Tiles) do
-                        l[#l + 1] = { pos_str = pos_str, data = data, }
-                    end
-                    
-                    if next(l) then
-                        local picked
-                        local tries = 0
-                        local camera = GetPlayerCameraTransform()
-                        repeat
-                            picked = l[math.random(#l)]
-                            tries = tries + 1
-
-                            local p = GetWorld(picked.pos_str)
-                        until AutoVecDist(ORIGIN, p) > SAFE_DISTANCE and not AutoPointInView(p, camera) or tries >= 8
-                        
-                        local path = false
-                        if not NOPATH then
-                            path = GetNodeBacktrace(picked.data.node)
-                            table.insert(path, 1, ORIGIN)
-                        end
-            
-                        local bias = {}
-                        for i = #SPAWN_PATH, 1, -1 do
-                            bias[#bias+1] = i
-                        end
-
-                        local handles = SpawnZombie(SPAWN_PATH[AutoBias(bias)], Transform(VecAdd(GetWorld(picked.pos_str), Vec(0, 0.8)), QuatEuler(0, math.random() * 360)), true, path, true)
-                        table.insert(ZOMBIES, handles[1])
-                    end
-                end
-
-                Last_Zombie_Spawn_Time = GetTime()
-            end
-        end
-    end
-end
-
-function draw()
-    -- if DEBUG.network and NETWORK then DrawNodeFwdtrace(NETWORK) end
-    -- if DEBUG.map then
-    --     -- DrawTileConnections(MAP.Explored_Tiles)
-    --     -- DrawTileBoxes(MAP.Edge_Tiles, { 0, 1, 0, 0.5 })
-    --     -- DrawTileBoxes(MAP.Wall_Tiles, { 1, 0, 0, 0.5 })
-    --     DrawTileConnections(MAP.Wall_Tiles)
-    -- end
-
-    -- local pos = AutoRaycastCamera(true, 128, 0, true).intersection
-    -- local tile, tile_pos_str = GetTileAtWorldPos(MAP.Explored_Tiles, pos)
-    -- if not tile then
-    --     tile, tile_pos_str = GetTileAtWorldPos(MAP.Explored_Tiles, VecAdd(pos, Vec(0, MAP.Tile_Size)))
-    -- end
-        
-    -- if tile then
-    --     AutoDrawBox(GetWorld(tile_pos_str), MAP.Tile_Size / 2)
-
-    --     if tile.node then
-    --         DrawNodeBacktrace(tile.node)
-    --         DebugLine(GetWorld(tile_pos_str), GetWorld(tile.node.pos_str), AutoHSVToRGB(tile.hue, 0.75, 1))
-    --     end
-    -- end
 end
 
 function Explore()
@@ -343,9 +151,6 @@
     return new_tile
 end
 
----@param cache table
----@param pos_str string
----@param check_strs table<any, vector>
 function AddToConditionCache(cache, pos_str, check_strs, in_list)
     for name, o in pairs(check_strs) do
         local data = {}
@@ -511,4 +316,139 @@
     ParticleColor(AutoHSVToRGB(hue, 0.8, 1))
 
     SpawnParticle(pos, Vec(), time or 1)
-end+end
+
+function server.init()
+    ORIGIN = Vec()
+    MAP = {
+        Tile_Size = 0.6,
+        ---@type tile[]
+        Explored_Tiles = {},
+        ---@type tile[]
+        Unexplored_Tiles = {},
+        ---@type tile[]
+        Ground_Tiles = {},
+        ---@type tile[]
+        Wall_Tiles = {},
+        ---@type tile[]
+        Edge_Tiles = {},
+    }
+    Last_Zombie_Spawn_Time = -1/0
+    ZOMBIES = {}
+    ---@type node
+    ---@diagnostic disable-next-line
+    NETWORK = false
+    DEBUG = {
+        network = false,
+        map = false,
+        queries = true,
+    }
+    NEIGHBOR = {
+        ortho_horizontal =      { Vec(-1, 0, 0), Vec(1, 0, 0), Vec(0, 0, -1), Vec(0, 0, 1), },
+        all_horizontal =        { Vec(-1, 0, 0), Vec(1, 0, 0), Vec(0, 0, -1), Vec(0, 0, 1), Vec(-1, 0, -1), Vec(1, 0, -1), Vec(-1, 0, -1), Vec(-1, 0, 1), },
+        up_middle_down =        { down = Vec(0, -1), up = Vec(0, 1), middle = Vec() },
+    }
+    SPAWN_PATH = AutoSplit(GetStringParam('spawn', 'MOD/xml/default.xml'), ',')
+    Interval = GetFloatParam('interval', 2)
+    NOPATH = GetBoolParam('nopath', false)
+    QUERY_REQUIREMENTS = 'physical large'
+    SAFE_DISTANCE = 5
+    SCRIPT_HANDLE = AutoGetScriptHandle()
+    C_Explore = coroutine.create(Explore)
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString('game.player.tool') == 'none' then
+        ORIGIN = AutoRaycast(AutoRaycastCamera(true, 150, 0, true).intersection, Vec(0, -1), 128, 0.1).intersection
+
+        ParticleLine(VecAdd(ORIGIN, Vec(math.cos(GetTime() * 22) * 0.25, 1, math.sin(GetTime() * 22) * 0.25)), ORIGIN, GetTime() / 3, GetTime() / 3, 2)
+
+        if not InputDown('shift') then
+            SAFE_DISTANCE = AutoClamp(SAFE_DISTANCE + InputValue('mousewheel'), 1, 20)
+        end
+
+        local v1 = Vec(SAFE_DISTANCE, 0, 0)
+        for t = 0, math.pi * 2, math.pi / 32 do
+            local v2 = Vec(math.cos(t) * SAFE_DISTANCE, 0, math.sin(t) * SAFE_DISTANCE)
+            DrawLine(VecAdd(ORIGIN, v1), VecAdd(ORIGIN, v2))
+            DrawLine(VecAdd(ORIGIN, v1), ORIGIN)
+            v1 = VecCopy(v2)
+        end
+
+        SetBool('game.disablepause', true, true)
+        if InputPressed('esc') then
+            SignScriptUpForRemoval(SCRIPT_HANDLE)
+        end
+    else
+        -- if InputPressed('y') then
+        --     SignUpForRemoval(SCRIPT_HANDLE)
+        -- end
+
+        -- if InputPressed('u') then
+        --     DEBUG.network = not DEBUG.network
+        -- end
+
+        -- if InputPressed('i') then
+        --     DEBUG.map = not DEBUG.map
+        -- end
+
+        if AutoPrimaryMenuButton('Kill Spawner') then
+            SignScriptUpForRemoval(SCRIPT_HANDLE)
+        end
+
+        if C_Explore then
+            if coroutine.status(C_Explore) == "suspended" then coroutine.resume(C_Explore) end
+
+            SetBool('game.disablepause', true, true)
+            if InputPressed('esc') or coroutine.status(C_Explore) == "dead" then
+                C_Explore = nil
+            end
+        else
+            if GetTime() - Last_Zombie_Spawn_Time > Interval then
+                for i, script in pairs(ZOMBIES) do
+                    if GetTagValue(script, 'status') ~= 'alive' then
+                        table.remove(ZOMBIES, i)
+                    end
+                end
+
+                if #ZOMBIES < 15 then
+                    local l = {}
+
+                    for pos_str, data in pairs(MAP.Explored_Tiles) do
+                        l[#l + 1] = { pos_str = pos_str, data = data, }
+                    end
+
+                    if next(l) then
+                        local picked
+                        local tries = 0
+                        local camera = GetPlayerCameraTransform(playerId)
+                        repeat
+                            picked = l[math.random(#l)]
+                            tries = tries + 1
+
+                            local p = GetWorld(picked.pos_str)
+                        until AutoVecDist(ORIGIN, p) > SAFE_DISTANCE and not AutoPointInView(p, camera) or tries >= 8
+
+                        local path = false
+                        if not NOPATH then
+                            path = GetNodeBacktrace(picked.data.node)
+                            table.insert(path, 1, ORIGIN)
+                        end
+
+                        local bias = {}
+                        for i = #SPAWN_PATH, 1, -1 do
+                            bias[#bias+1] = i
+                        end
+
+                        local handles = SpawnZombie(SPAWN_PATH[AutoBias(bias)], Transform(VecAdd(GetWorld(picked.pos_str), Vec(0, 0.8)), QuatEuler(0, math.random() * 360)), true, path, true)
+                        table.insert(ZOMBIES, handles[1])
+                    end
+                end
+
+                Last_Zombie_Spawn_Time = GetTime()
+            end
+        end
+    end
+end
+

```

---

# Migration Report: script\Zcmd\pipe_lua.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zcmd\pipe_lua.lua
+++ patched/script\Zcmd\pipe_lua.lua
@@ -1,23 +1,16 @@
---[[
-#include ../Automatic.lua
-#include ../CONFIG.lua
-#include ../Zhelper.lua
-]]
-
-function init()
+#version 2
+function server.init()
     local z = {}
-
     for _, b in pairs(FindBodies(zombie_scheme, true)) do
         local script_handle = tonumber(GetTagValue(b, zombie_scheme))
         if GetTagValue(script_handle, 'status') ~= 'dead' then
             z[script_handle] = true
         end
     end
-
     local lua = GetStringParam('lua')
     for handle in pairs(z) do
         SignUpLua(handle, lua)
     end
+    SignScriptUpForRemoval(AutoGetScriptHandle())
+end
 
-    SignScriptUpForRemoval(AutoGetScriptHandle())
-end
```

---

# Migration Report: script\Zcmd\ui_pipe_lua.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zcmd\ui_pipe_lua.lua
+++ patched/script\Zcmd\ui_pipe_lua.lua
@@ -1,19 +1,6 @@
---[[
-#include ../Automatic.lua
-#include ../CONFIG.lua
-#include ../Zhelper.lua
-]]
-
+#version 2
 local editting = true
 local lua = ''
-
----@type key[]
-detect_keys = {
-    'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
-    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', ',', '-',
-    'space', 'backspace', 'delete'
-}
-
 local specials = {
     ['.'] = '>',
     [','] = '<',
@@ -59,7 +46,24 @@
     UiText(str)
 end
 
-function draw()
+function finish()
+    local z = {}
+
+    for _, b in pairs(FindBodies(zombie_scheme, true)) do
+        local script_handle = tonumber(GetTagValue(b, zombie_scheme))
+        if GetTagValue(script_handle, 'status') ~= 'dead' then
+            z[script_handle] = true
+        end
+    end
+
+    for handle in pairs(z) do
+        SignUpLua(handle, lua)
+    end
+
+    SignScriptUpForRemoval(AutoGetScriptHandle())
+end
+
+function client.draw()
     if GetString('game.player.tool') ~= 'none' then
         finish()
     elseif editting then
@@ -76,19 +80,3 @@
     CoolText(lua)
 end
 
-function finish()
-    local z = {}
-
-    for _, b in pairs(FindBodies(zombie_scheme, true)) do
-        local script_handle = tonumber(GetTagValue(b, zombie_scheme))
-        if GetTagValue(script_handle, 'status') ~= 'dead' then
-            z[script_handle] = true
-        end
-    end
-
-    for handle in pairs(z) do
-        SignUpLua(handle, lua)
-    end
-
-    SignScriptUpForRemoval(AutoGetScriptHandle())
-end
```

---

# Migration Report: script\Zcompatability.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zcompatability.lua
+++ patched/script\Zcompatability.lua
@@ -1,9 +1,4 @@
---[[
-#include "loadpatch.lua"
-]]
-
-zombie_mod_id = Loader.mod_id
-
+#version 2
 local needed_files = {
     'script/Automatic.lua',
     'script/shape_utils.lua',
@@ -12,14 +7,8 @@
     'script/Zhelper.lua',
     'script/Zlocal.lua',
 }
-
--------- Including --------
-
 local mod_path = GetString(('mods.available.%s.path'):format(zombie_mod_id))
 
----Merges two tables together, does not return anything
----@param base table
----@param overwrite table
 function AutoTableMerge(base, overwrite)
 	for k, v in pairs(overwrite) do
 		if type(v) == "table" then
@@ -34,26 +23,3 @@
 	end
 end
 
-for i=1, #needed_files do
-    local overwrite_file_path = string.format('%s/%s', mod_path, needed_files[i])
-    
-    if HasFile('RAW:' .. overwrite_file_path) then
-        local f = assert(loadfile(overwrite_file_path))
-        
-        local env = {}
-        setmetatable(env, {
-            __index = _G
-        })
-        
-        setfenv(f, env)
-        local success, result = pcall(f)
-        if success then
-            AutoTableMerge(_G, env)
-            print(('Zcompatability.lua : Succesfully Loaded "%s"'):format(overwrite_file_path))
-        else
-            print(('Zcompatability.lua : Failed Injecting [%s]; Error [%s]'):format(overwrite_file_path, result))
-        end
-    else
-        print(('Zcompatability.lua : Could not find file at path "%s"'):format(overwrite_file_path))
-    end
-end

```

---

# Migration Report: script\Zglobal.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zglobal.lua
+++ patched/script\Zglobal.lua
@@ -1,16 +1,8 @@
---[[
-#include Automatic.lua
-#include pal.lua
-#include CONFIG.lua
-#include Zhelper.lua
-]]
-
-function init()
-    SetBool(zombie_global_key, true)
-
+#version 2
+function server.init()
+    SetBool(zombie_global_key, true, true)
     Blood_T = {}
     Add_Blood_To_Shapes = {}
-
     Camera = {
         enabled = false,
         was_invisible = false,
@@ -23,22 +15,130 @@
         },
         toggle_LT = -1/0
     }
-
     Keybinds = {
         Anchor = 'c',
     }
 end
 
-function tick()
-    local Time = GetTime()
-    
-    local force_set_camera = false
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local Time = GetTime()
+        local force_set_camera = false
+        local shape_transform = GetShapeWorldTransform(Camera.shape)
+        if GetShapeVoxelCount(Camera.shape) <= 0 then
+            Camera.shape_last_known_transform = TransformCopy(shape_transform)
+        end
+        local world_transform_target = TransformToParentTransform(shape_transform, Camera.relative_transform)
+        world_transform_target.rot = QuatSlerp(world_transform_target.rot, QuatLookAt(world_transform_target.pos, GetPlayerCameraTransform(playerId).pos), 0.55)
+        local update_function = force_set_camera and AutoSM_Set or AutoSM_Update
+        update_function(Camera.SM.pos, world_transform_target.pos)
+        local vel = VecLength(AutoSM_GetVelocity(Camera.SM.pos))
+        AutoSM_AddVelocity(Camera.SM.rot, AutoRandomQuat(vel / 2.5 ^ 4))
+        update_function(Camera.SM.rot, world_transform_target.rot)
+        if Camera.enabled then
+            local t = {
+                pos = AutoSM_Get(Camera.SM.pos),
+                rot = AutoSM_Get(Camera.SM.rot),
+            }
 
+            SetCameraTransform(t)
+            SetBool('game.disable_weighted_camera', true, true)
+
+            if HasTag(Camera.shape, 'dead') then
+                SetCameraDof(1, 2)
+            else
+                SetCameraDof(10, vel / 10)
+            end
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for _, key in pairs(ListKeys(zombie_handle_cleanup)) do
+            local full_key = AutoKey(zombie_handle_cleanup, key)
+            Delete(GetInt(full_key))
+            ClearKey(full_key)
+        end
+        --- Add Blood_Indicies
+        for _, key in pairs(ListKeys(zombie_add_blood_indicies)) do
+            local full_key = AutoKey(zombie_add_blood_indicies, key)
+            local str = GetString(full_key)
+            local handles = AutoSplit(str, ' ', true)
+            local T = {}
+            for _, h in pairs(handles) do
+                if IsHandleValid(h) then
+                    T[#T + 1] = h
+                end
+            end
+
+            Add_Blood_To_Shapes[#Add_Blood_To_Shapes + 1] = T
+
+            ClearKey(full_key)
+        end
+        --- Blood
+        for _, key in pairs(ListKeys(zombie_blood_key)) do
+            local full_key = AutoKey(zombie_blood_key, key)
+            local str = GetString(full_key)
+            local param = AutoSplit(str, ' ', true)
+            Blood_T[#Blood_T + 1] = param
+
+            ClearKey(full_key)
+        end
+        -- Handle Adding Blood To Shapes
+        for i = 1, 8 do
+            local SS = Add_Blood_To_Shapes[i]
+            if not SS then break end
+
+            ForcePopulateBloodIndicies(SS)
+
+            table.remove(Add_Blood_To_Shapes, i)
+        end
+
+        -- Handle Blood
+        -- local z_parts = FindBodies(zombie_scheme, true)
+        local reject = {}
+        local tool_shapes = GetBodyShapes(GetToolBody())
+        local tool_transform = GetBodyTransform(GetToolBody())
+
+        for i = 1, 4 do
+            local B = Blood_T[i]
+            if not B then break end
+
+            for _ = 1, 3 do
+                -- AutoQueryRejectBodies(z_parts)
+                AutoQueryRejectBodies(reject)
+
+                local ray = AutoRaycast(B, QuatRotateVec(AutoRandomQuat(65 + math.random() * 25), Vec(0, -1)), 12)
+                if #tool_shapes < 8 and AutoVecDist(tool_transform.pos, B) < 1 then
+                    for _, s in pairs(tool_shapes) do
+                        PaintBlood(s, B, ({ 6, 4, 3 })[AutoBias({ 2, 1, 1 })])
+                    end
+                end
+
+                if ray.hit then
+                    if not AutoTableContains(tool_shapes, ray.shape) then
+                        PaintBlood(ray.shape, ray.intersection, ({ 6, 4, 3 })[AutoBias({ 2, 1, 1 })])
+                    end
+
+                    if HasTag(ray.body, zombie_scheme) then
+                        reject[#reject + 1] = ray.body
+                    end
+                end
+            end
+
+            table.remove(Blood_T, i)
+        end
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
     if Camera.enabled then
         if InputPressed(Keybinds.Anchor) then
             Camera.enabled = false
             Camera.toggle_LT = Time
-        
+
             if not Camera.was_invisible then
                 RemoveTag(Camera.shape, 'invisible')
             end
@@ -64,7 +164,7 @@
                 Camera.shape = best.shape
                 local shape_transform = GetShapeWorldTransform(best.shape)
                 Camera.relative_transform = TransformToLocalTransform(shape_transform, Transform(best.center, GetBodyTransform(GetShapeBody(best.shape)).rot))
-    
+
                 force_set_camera = true
                 Camera.enabled = true
                 Camera.toggle_LT = Time
@@ -73,126 +173,14 @@
             end
         end
     end
-
-    
-    local shape_transform = GetShapeWorldTransform(Camera.shape)
-    if GetShapeVoxelCount(Camera.shape) <= 0 then
-        Camera.shape_last_known_transform = TransformCopy(shape_transform)
-    end
-
-    local world_transform_target = TransformToParentTransform(shape_transform, Camera.relative_transform)
-    world_transform_target.rot = QuatSlerp(world_transform_target.rot, QuatLookAt(world_transform_target.pos, GetPlayerCameraTransform().pos), 0.55)
-    
-    local update_function = force_set_camera and AutoSM_Set or AutoSM_Update
-    update_function(Camera.SM.pos, world_transform_target.pos)
-
-    local vel = VecLength(AutoSM_GetVelocity(Camera.SM.pos))
-    AutoSM_AddVelocity(Camera.SM.rot, AutoRandomQuat(vel / 2.5 ^ 4))
-    update_function(Camera.SM.rot, world_transform_target.rot)
-
-    if Camera.enabled then
-        local t = {
-            pos = AutoSM_Get(Camera.SM.pos),
-            rot = AutoSM_Get(Camera.SM.rot),
-        }
-
-        SetCameraTransform(t)
-        SetBool('game.disable_weighted_camera', true)
-
-        if HasTag(Camera.shape, 'dead') then
-            SetCameraDof(1, 2)
-        else
-            SetCameraDof(10, vel / 10)
-        end
-    end
 end
 
-function update()
-    --- Handle Cleanup
-    for _, key in pairs(ListKeys(zombie_handle_cleanup)) do
-        local full_key = AutoKey(zombie_handle_cleanup, key)
-        Delete(GetInt(full_key))
-        ClearKey(full_key)
-    end
-
-    --- Add Blood_Indicies
-    for _, key in pairs(ListKeys(zombie_add_blood_indicies)) do
-        local full_key = AutoKey(zombie_add_blood_indicies, key)
-        local str = GetString(full_key)
-        local handles = AutoSplit(str, ' ', true)
-        local T = {}
-        for _, h in pairs(handles) do
-            if IsHandleValid(h) then
-                T[#T + 1] = h
-            end
-        end
-
-        Add_Blood_To_Shapes[#Add_Blood_To_Shapes + 1] = T
-
-        ClearKey(full_key)
-    end
-
-    --- Blood
-    for _, key in pairs(ListKeys(zombie_blood_key)) do
-        local full_key = AutoKey(zombie_blood_key, key)
-        local str = GetString(full_key)
-        local param = AutoSplit(str, ' ', true)
-        Blood_T[#Blood_T + 1] = param
-
-        ClearKey(full_key)
-    end
-
-    -- Handle Adding Blood To Shapes
-    for i = 1, 8 do
-        local SS = Add_Blood_To_Shapes[i]
-        if not SS then break end
-
-        ForcePopulateBloodIndicies(SS)
-
-        table.remove(Add_Blood_To_Shapes, i)
-    end
-
-    -- Handle Blood
-    -- local z_parts = FindBodies(zombie_scheme, true)
-    local reject = {}
-    local tool_shapes = GetBodyShapes(GetToolBody())
-    local tool_transform = GetBodyTransform(GetToolBody())
-
-    for i = 1, 4 do
-        local B = Blood_T[i]
-        if not B then break end
-
-        for _ = 1, 3 do
-            -- AutoQueryRejectBodies(z_parts)
-            AutoQueryRejectBodies(reject)
-
-            local ray = AutoRaycast(B, QuatRotateVec(AutoRandomQuat(65 + math.random() * 25), Vec(0, -1)), 12)
-            if #tool_shapes < 8 and AutoVecDist(tool_transform.pos, B) < 1 then
-                for _, s in pairs(tool_shapes) do
-                    PaintBlood(s, B, ({ 6, 4, 3 })[AutoBias({ 2, 1, 1 })])
-                end
-            end
-
-            if ray.hit then
-                if not AutoTableContains(tool_shapes, ray.shape) then
-                    PaintBlood(ray.shape, ray.intersection, ({ 6, 4, 3 })[AutoBias({ 2, 1, 1 })])
-                end
-
-                if HasTag(ray.body, zombie_scheme) then
-                    reject[#reject + 1] = ray.body
-                end
-            end
-        end
-
-        table.remove(Blood_T, i)
-    end
-end
-
-function draw()
+function client.draw()
     local diff = GetTime() - Camera.toggle_LT
     local t = AutoSigmoid(diff, 2, 10, 0)
     UiColor(0, 0, 0, t)
     if t > 1e-3 then
         UiRect(AutoUiBounds())
     end
-end+end
+

```

---

# Migration Report: script\Zhelper.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zhelper.lua
+++ patched/script\Zhelper.lua
@@ -1,3 +1,4 @@
+#version 2
 function SignScriptUpForRemoval(handle)
     local dummy = function() end
     init = dummy
@@ -6,12 +7,12 @@
     update = dummy
     draw = dummy
 
-    SetString(AutoKey(zombie_handle_cleanup, #ListKeys(zombie_handle_cleanup)), handle)
+    SetString(AutoKey(zombie_handle_cleanup, #ListKeys(zombie_handle_cleanup)), handle, true)
 end
 
 function SignUpLua(zombie_script, luastr)
     local pipe = AutoKey(zombie_lua_pipe, zombie_script)
-    SetString(AutoKey(pipe, #ListKeys(pipe) + 1), luastr)
+    SetString(AutoKey(pipe, #ListKeys(pipe) + 1), luastr, true)
 end
 
 function RejectAllZombies()
@@ -19,7 +20,7 @@
 end
 
 function SignUpForBloodIndicies(shapes)
-	SetString(AutoKey(zombie_add_blood_indicies, #ListKeys(zombie_add_blood_indicies)), table.concat(shapes, ' '))
+	SetString(AutoKey(zombie_add_blood_indicies, #ListKeys(zombie_add_blood_indicies)), table.concat(shapes, ' '), true)
 end
 
 function PaintBlood(shape, pos, size)
@@ -58,7 +59,6 @@
     return indicies
 end
 
---- t is -1 to 1, when less than or equal to zero, use a and b, otherwise use b and c
 function SplitLerp(a, b, c, t)
     if t <= 0 then return AutoLerp(a, b, t + 1) else return AutoLerp(b, c, t) end
 end
@@ -82,4 +82,5 @@
     if path then SetTag(e[1], 'inject path', path_str) end
 
     return e
-end+end
+

```

---

# Migration Report: script\Zlocal.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zlocal.lua
+++ patched/script\Zlocal.lua
@@ -1,16 +1,4 @@
---[[
-#include Automatic.lua
-#include pal.lua
-#include CONFIG.lua
-#include Zhelper.lua
-]]
-
--------------------------------- BASE --------------------------------
-Z = {}
-INJECT = {}
-
--------------------------------- INJECTION --------------------------------
-
+#version 2
 function Load_Injection(show_debug)
 	--- This first section is just for the user setting `ip_mod_id` and `ip_file_name`
 	local inject_param = GetStringParam('inject', 'NOTHING TO INJECT')
@@ -59,22 +47,6 @@
 	Fullinject(ip_mod_id, ip_file_name, show_debug)
 end
 
-Load_Injection(false)
-
-if INJECT.OVERRIDE then return INJECT.OVERRIDE() end
-
-if not INJECT.PROFILE then print('No profile defined, returning; INJECT = ' .. AutoToString(INJECT, 2)) return else PROFILE = INJECT.PROFILE end
-
--------------------------------- SCRIPT BASE --------------------------------
-function init(...)
-    if INJECT.OVERRIDE_INIT then return INJECT.OVERRIDE_INIT(...) end
-
-    ZombieSetup()
-    ZombiePreUpdate()
-
-    if INJECT.CB_INIT then INJECT.CB_INIT(...) end
-end
-
 function handleCommand(...)
     if INJECT.OVERRIDE_HANDLECOMMAND then return INJECT.OVERRIDE_HANDLECOMMAND(...) end
 
@@ -85,55 +57,6 @@
 	if INJECT.CB_HANDLECOMMAND then INJECT.CB_HANDLECOMMAND(...) end
 end
 
-function tick(...)
-    if INJECT.OVERRIDE_TICK then return INJECT.OVERRIDE_TICK(...) end
-
-	do
-		for _, H in pairs(ListKeys(zombie_lua_pipe)) do
-			if tonumber(H) == Z.script then
-				local K = AutoKey(zombie_lua_pipe, H)
-                for _, L in pairs(ListKeys(K)) do
-                    local KL = AutoKey(K, L)
-                    local lua = GetString(KL)
-
-                    pcall(select(2, pcall(loadstring, lua)))
-                    ClearKey(KL)
-                end
-				
-				ClearKey(K)
-				break
-			end
-		end
-	end
-	
-	if INJECT.CB_SHAPE_LOOP_TICK then
-		for handle, data in pairs(Z.shape_data) do
-			if IsHandleValid(handle) then
-				INJECT.CB_SHAPE_LOOP_TICK(handle, data, ...)
-			end
-		end
-	end
-	
-	ZombieTick(...)
-
-    if INJECT.CB_TICK then INJECT.CB_TICK(...) end
-end
-
-function update(...)
-    if INJECT.OVERRIDE_UPDATE then return INJECT.OVERRIDE_UPDATE(...) end
-
-	ZombieUpdate(...)
-
-    if INJECT.CB_UPDATE then INJECT.CB_UPDATE(...) end
-end
-
-function draw(...)
-    if INJECT.OVERRIDE_DRAW then return INJECT.OVERRIDE_DRAW(...) end
-
-    if INJECT.CB_DRAW then INJECT.CB_DRAW(...) end
-end
-
--------------------------------- ZOMBIE BASE --------------------------------
 function ZombieSetup()
     if not HasKey(zombie_global_key) then
         AutoSpawnScript('RAW:' .. zombie_root .. '/script/Zglobal.lua')
@@ -293,7 +216,7 @@
 	-------------------------------- Setup --------------------------------
     local hostile = GetTagValue(Z.script, 'hostile') == '1'
 	
-	local player = GetPlayerTransform()
+	local player = GetPlayerTransform(playerId)
 	
 	local health_percentage = Z.Mem.health / Z.Mem.max_health
 	local submerged = Z.body_data.Head.center and IsPointInWater(Z.body_data.Head.center)
@@ -322,7 +245,7 @@
 	local eyes = Transform(Z.body_data.Head.center, GetBodyTransform(Z.body_data.Head.handle).rot)
 	
 	RejectAllZombies()
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	local seen_ray = AutoRaycastTo(eyes.pos, VecAdd(player.pos, Vec(0, 1)))
 	local seen_fov = AutoPointToAngle(player.pos, eyes)
 	Z.Mem.seen_by_player = not seen_ray.hit
@@ -566,7 +489,7 @@
 	
 		if Z.Sounds and Z.Sounds.damage and (GetTime() - Z.Mem.damage_LT > 0.5) then PlaySound(Z.Sounds.damage, center, 2) end
 	
-		SetString(AutoKey(zombie_blood_key, #ListKeys(zombie_blood_key)), table.concat(center, ' '))
+		SetString(AutoKey(zombie_blood_key, #ListKeys(zombie_blood_key)), table.concat(center, ' '), true)
 		
 		ParticleReset()
 	
@@ -602,7 +525,6 @@
 	Z.Mem.damage_LT = GetTime()
 end
 
--------------------------------- UTILITIY --------------------------------
 function RejectSelf()
     for s, _ in pairs(Z.shape_data) do
         QueryRejectShape(s)
@@ -626,4 +548,63 @@
 
 function ClearPathQueue()
     Z.path_queue = {}
-end+end
+
+function server.init()
+    if INJECT.OVERRIDE_INIT then return INJECT.OVERRIDE_INIT(...) end
+
+    ZombieSetup()
+    ZombiePreUpdate()
+
+    if INJECT.CB_INIT then INJECT.CB_INIT(...) end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+           if INJECT.OVERRIDE_TICK then return INJECT.OVERRIDE_TICK(...) end
+
+        do
+        	for _, H in pairs(ListKeys(zombie_lua_pipe)) do
+        		if tonumber(H) == Z.script then
+        			local K = AutoKey(zombie_lua_pipe, H)
+                       for _, L in pairs(ListKeys(K)) do
+                           local KL = AutoKey(K, L)
+                           local lua = GetString(KL)
+
+                           pcall(select(2, pcall(loadstring, lua)))
+                           ClearKey(KL)
+                       end
+
+        			ClearKey(K)
+        			break
+        		end
+        	end
+        end
+        if INJECT.CB_SHAPE_LOOP_TICK then
+        	for handle, data in pairs(Z.shape_data) do
+        		if IsHandleValid(handle) then
+        			INJECT.CB_SHAPE_LOOP_TICK(handle, data, ...)
+        		end
+        	end
+        end
+        ZombieTick(...)
+           if INJECT.CB_TICK then INJECT.CB_TICK(...) end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+           if INJECT.OVERRIDE_UPDATE then return INJECT.OVERRIDE_UPDATE(...) end
+
+        ZombieUpdate(...)
+
+           if INJECT.CB_UPDATE then INJECT.CB_UPDATE(...) end
+    end
+end
+
+function client.draw()
+    if INJECT.OVERRIDE_DRAW then return INJECT.OVERRIDE_DRAW(...) end
+
+    if INJECT.CB_DRAW then INJECT.CB_DRAW(...) end
+end
+

```

---

# Migration Report: script\Zspec\buff.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zspec\buff.lua
+++ patched/script\Zspec\buff.lua
@@ -1,45 +1 @@
-Zinject 'script/Automatic.lua'
-Zinject 'script/Zspec/default.lua'
-
-PROFILE = {
-    Weights = {
-        Chest =             { impulse = 1, 		apply_tags = { } },
-        Head =              { impulse = 1.25, 	apply_tags = { } },
-        ArmLeft =           { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        HandLeft =          { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        ArmRight =          { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        HandRight =         { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        Hips =              { impulse = 1.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegLeftUpper =      { impulse = 1.25, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegLeftLower =      { impulse = 1.25, 	apply_tags = { } },
-        FootLeft =			{ impulse = 0.75, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegRightUpper =		{ impulse = 1.25, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegRightLower =		{ impulse = 1.25, 	apply_tags = { } },
-        FootRight =			{ impulse = 0.75, 	apply_tags = { { 'SP_IGNORE' } } },
-    },
-    Color = AutoColors.green_light,
-	Raise_Arms = true,
-    Tweaks = {
-        impulse_strength = 35,
-        speed = 7.5,
-        foot_move_impulse = 25,
-        hip_move_impulse = 5,
-        orientation_randomness_scale = 0.75,
-        orientation_change_interval = 0.167,
-        step_interval = 0.4175,
-        bite_interval = 0.55,
-        bite_damage = 1 / 3,
-        focus_end_distance = 0.65,
-        checkpoint_distance = 0.5,
-        focus_give_up_time = 4,
-        eye_half_fov = 55,
-        tag_on_unlink = 'SP_IGNORE'
-    },
-    Sounds = {
-        crunch = { LoadSound, 'MOD/snd/crunch-0.ogg', 6 },
-        damage = { LoadSound, 'MOD/snd/growl-0.ogg', 8 },
-        whine = { LoadLoop, 'MOD/snd/whine.ogg', 7 },
-        death = { LoadSound, 'MOD/snd/growl-0.ogg', 8 },
-        step = false,
-    }
-}+#version 2

```

---

# Migration Report: script\Zspec\cellshader.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zspec\cellshader.lua
+++ patched/script\Zspec\cellshader.lua
@@ -1,49 +1,4 @@
-Zinject 'script/Automatic.lua'
-Zinject 'script/Zspec/default.lua'
-
-PROFILE = {
-    Weights = {
-        Chest =             { impulse = 1, 		apply_tags = { { 'autobreak' }, } },
-        Head =              { impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        ArmLeft =           { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        HandLeft =          { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        ArmRight =          { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        HandRight =         { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        Hips =              { impulse = 1.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegLeftUpper =      { impulse = 1.25, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegLeftLower =      { impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        FootLeft =			{ impulse = 0.75, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegRightUpper =		{ impulse = 1.25, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegRightLower =		{ impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        FootRight =			{ impulse = 0.75, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-    },
-    Color = AutoColors.green_light,
-	Raise_Arms = true,
-    Tweaks = {
-        impulse_strength = 20,
-        speed = 7.5,
-        foot_move_impulse = 25,
-        hip_move_impulse = 5,
-        orientation_randomness_scale = 0.75,
-        orientation_change_interval = 0.1,
-        step_interval = 0.25,
-        bite_interval = 0.55,
-        bite_damage = 1 / 3,
-        focus_end_distance = 0.65,
-        checkpoint_distance = 0.5,
-        focus_give_up_time = 4,
-        eye_half_fov = 55,
-        tag_on_unlink = 'SP_IGNORE'
-    },
-    Sounds = {
-        crunch = { LoadSound, 'MOD/snd/crunch-0.ogg', 6 },
-        damage = { LoadSound, 'MOD/snd/growl-0.ogg', 8 },
-        whine = { LoadLoop, 'MOD/snd/whine.ogg', 7 },
-        death = { LoadSound, 'MOD/snd/growl-0.ogg', 8 },
-        step = false,
-    }
-}
-
+#version 2
 function CB_SHAPE_LOOP_TICK(handle, data, dt)
     SetTag(handle, 'invisible')
 
@@ -56,7 +11,7 @@
         f.rot = QuatRotateQuat(f.rot, QuatEuler(0, 0, math.random(0, 1) * 180))
         
         local dot = VecDot(VecSub(f.pos, camera.pos), forward)
-        if dot > 0 then
+        if dot ~= 0 then
             local half_size_increase = 0
             local shader_color = VecLerp(AutoColors.alert_dark, AutoColors.green_light, (VecDot(AutoTransformFwd(f), Vec(0, 1)) / 2 + 1) ^ 2)
             DrawSprite(AutoFlatSprite,
@@ -81,4 +36,5 @@
     for handle, data in pairs(Z.shape_data) do
         RemoveTag(handle, 'invisible')
     end
-end+end
+

```

---

# Migration Report: script\Zspec\clouds.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zspec\clouds.lua
+++ patched/script\Zspec\clouds.lua
@@ -1,45 +1 @@
-Zinject 'script/Automatic.lua'
-Zinject 'script/Zspec/default.lua'
-
-PROFILE = {
-    Weights = {
-        Chest =             { impulse = 1, 		apply_tags = { { 'autobreak' }, } },
-        Head =              { impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        ArmLeft =           { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        HandLeft =          { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        ArmRight =          { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        HandRight =         { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        Hips =              { impulse = 1.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegLeftUpper =      { impulse = 2,  	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegLeftLower =      { impulse = 3,  	apply_tags = { { 'autobreak' }, } },
-        FootLeft =			{ impulse = 1,  	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegRightUpper =		{ impulse = 2,  	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegRightLower =		{ impulse = 3,  	apply_tags = { { 'autobreak' }, } },
-        FootRight =			{ impulse = 1, 	    apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-    },
-    Color = AutoColors.green_light,
-	Raise_Arms = true,
-    Tweaks = {
-        impulse_strength = 25,
-        speed = 7.5,
-        foot_move_impulse = 25,
-        hip_move_impulse = 10,
-        orientation_randomness_scale = 0.45,
-        orientation_change_interval = 0.167,
-        step_interval = 0.5,
-        bite_interval = 0.6,
-        bite_damage = 1 / 3,
-        focus_end_distance = 0.65,
-        checkpoint_distance = 0.5,
-        focus_give_up_time = 4,
-        eye_half_fov = 55,
-        tag_on_unlink = 'SP_IGNORE'
-    },
-    Sounds = {
-        crunch = { LoadSound, 'MOD/snd/crunch-0.ogg', 6 },
-        damage = { LoadSound, 'MOD/snd/growl-0.ogg', 8 },
-        whine = { LoadLoop, 'MOD/snd/whine.ogg', 7 },
-        death = { LoadSound, 'MOD/snd/growl-0.ogg', 8 },
-        step = false,
-    }
-}+#version 2

```

---

# Migration Report: script\Zspec\default.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zspec\default.lua
+++ patched/script\Zspec\default.lua
@@ -1,57 +1,15 @@
-Zinject 'script/Automatic.lua'
-
-PROFILE = {
-	Weights = {
-		Chest =             { impulse = 1, 		apply_tags = { { 'autobreak' }, } },
-		Head =              { impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-		ArmLeft =           { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-		HandLeft =          { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-		ArmRight =          { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-		HandRight =         { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-		Hips =              { impulse = 1.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-		LegLeftUpper =      { impulse = 1.25, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-		LegLeftLower =      { impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-		FootLeft =			{ impulse = 0.75, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-		LegRightUpper =		{ impulse = 1.25, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-		LegRightLower =		{ impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-		FootRight =			{ impulse = 0.75, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-	},
-	Color = AutoColors.green_light,
-	Raise_Arms = true,
-	Tweaks = {
-		impulse_strength = 20,
-		speed = 7.5,
-		foot_move_impulse = 10,
-		hip_move_impulse = 10,
-		orientation_randomness_scale = 0.6,
-		orientation_change_interval = 0.1,
-		step_interval = 0.25,
-		focus_end_distance = 0.65,
-		checkpoint_distance = 1,
-		focus_give_up_time = 4,
-		eye_half_fov = 55,
-		tag_on_unlink = 'SP_IGNORE'
-	},
-	Sounds = {
-		crunch = { LoadSound, 'MOD/snd/crunch-0.ogg', 6 },
-		damage = { LoadSound, 'MOD/snd/growl-0.ogg', 8 },
-		whine = { LoadLoop, 'MOD/snd/whine.ogg', 7 },
-		death = { LoadSound, 'MOD/snd/growl-0.ogg', 8 },
-		step = false,
-	}
-}
-
+#version 2
 local bite_lt = -1 / 0
 
 function HandleBiting(damage, interval)
 	local Time = GetTime()
-	local player = GetPlayerTransform()
+	local player = GetPlayerTransform(playerId)
 
 	-------------------------------- Bite --------------------------------
-	if Time - bite_lt > interval and GetPlayerVehicle() == 0 then
+	if Time - bite_lt > interval and GetPlayerVehicle(playerId) == 0 then
 		if AutoVecDist(Z.Mem.center, VecAdd(player.pos, Vec(0, 1.8/2))) < 0.65 then
-			local h = GetPlayerHealth()
-			SetPlayerHealth(h - damage)
+			local h = GetPlayerHealth(playerId)
+			SetPlayerHealth(playerId, h - damage)
 
 			ShakeCamera(0.5)
 			
@@ -64,4 +22,5 @@
 
 function CB_TICK()
     HandleBiting(1 / 3, 2 / 3)
-end+end
+

```

---

# Migration Report: script\Zspec\fae.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zspec\fae.lua
+++ patched/script\Zspec\fae.lua
@@ -1,44 +1,9 @@
-Zinject 'script/Automatic.lua'
-Zinject 'script/Zspec/default.lua'
-
-PROFILE = {
-    Weights = {
-        Chest =             { impulse = 1, 		apply_tags = { { 'autobreak' }, } },
-        Head =              { impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        ArmLeft =           { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        HandLeft =          { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        ArmRight =          { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        HandRight =         { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        Hips =              { impulse = 1.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegLeftUpper =      { impulse = 1.25, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegLeftLower =      { impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        FootLeft =			{ impulse = 0.75, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegRightUpper =		{ impulse = 1.25, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegRightLower =		{ impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        FootRight =			{ impulse = 0.75, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-    },
-    Color = { -1/0, -1/0, -1/0 },
-	Raise_Arms = true,
-    Tweaks = {
-        impulse_strength = 20,
-        speed = 7.5,
-        foot_move_impulse = 10,
-        hip_move_impulse = 10,
-        orientation_randomness_scale = 0.6,
-        orientation_change_interval = 0.1,
-        step_interval = 0.25,
-        focus_end_distance = 0.65,
-        checkpoint_distance = 1,
-        focus_give_up_time = 4,
-        eye_half_fov = 55,
-        tag_on_unlink = 'SP_IGNORE'
-    },
-}
-
+#version 2
 function CB_SHAPE_LOOP_TICK(handle, data, dt)
     DrawShapeHighlight(handle, 2)
 end
 
 function CB_TICK()
     HandleBiting(1 / 0, 1)
-end+end
+

```

---

# Migration Report: script\Zspec\glass.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zspec\glass.lua
+++ patched/script\Zspec\glass.lua
@@ -1,49 +1,5 @@
-Zinject 'script/Automatic.lua'
-Zinject 'script/Zspec/default.lua'
-
-PROFILE = {
-    Weights = {
-        Chest =             { impulse = 1, 		apply_tags = { } },
-        Head =              { impulse = 1.25, 	apply_tags = { } },
-        ArmLeft =           { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        HandLeft =          { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        ArmRight =          { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        HandRight =         { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        Hips =              { impulse = 1.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegLeftUpper =      { impulse = 1.25, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegLeftLower =      { impulse = 1.25, 	apply_tags = { } },
-        FootLeft =			{ impulse = 0.75, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegRightUpper =		{ impulse = 1.25, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegRightLower =		{ impulse = 1.25, 	apply_tags = { } },
-        FootRight =			{ impulse = 0.75, 	apply_tags = { { 'SP_IGNORE' } } },
-    },
-    Color = AutoColors.white,
-	Raise_Arms = true,
-    Tweaks = {
-        impulse_strength = 60,
-        speed = 5,
-        foot_move_impulse = 30,
-        hip_move_impulse = 20,
-        orientation_randomness_scale = 0.35,
-        orientation_change_interval = 0.125,
-        step_interval = 0.4,
-        bite_interval = 0.65,
-        bite_damage = 1 / 2,
-        focus_end_distance = 0.65,
-        checkpoint_distance = 0.5,
-        focus_give_up_time = 4,
-        eye_half_fov = 55,
-        tag_on_unlink = 'SP_IGNORE'
-    },
-    Sounds = {
-        crunch = { LoadSound, 'masonry/hit-s0.ogg', 6 },
-        damage = { LoadSound, 'masonry/break-m0', 6 },
-        whine = false,
-        death = { LoadSound, 'masonry/break-l0', 15 },
-        step = false,
-    }
-}
-
+#version 2
 function CB_DAMAGE(damaged_shape_handle, damaged_shape_data, voxels_removed)
     AutoLiquifyShape(damaged_shape_handle, false, true)
-end+end
+

```

---

# Migration Report: script\Zspec\impact.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zspec\impact.lua
+++ patched/script\Zspec\impact.lua
@@ -1,45 +1 @@
-Zinject 'script/Automatic.lua'
-Zinject 'script/Zspec/default.lua'
-
-PROFILE = {
-    Weights = {
-        Chest =             { impulse = 1, 		apply_tags = { } },
-        Head =              { impulse = 1.25, 	apply_tags = { } },
-        ArmLeft =           { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        HandLeft =          { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        ArmRight =          { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        HandRight =         { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        Hips =              { impulse = 1.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegLeftUpper =      { impulse = 1.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegLeftLower =      { impulse = 1.5, 	apply_tags = { } },
-        FootLeft =			{ impulse = 0.75, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegRightUpper =		{ impulse = 1.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegRightLower =		{ impulse = 1.5, 	apply_tags = { } },
-        FootRight =			{ impulse = 0.75, 	apply_tags = { { 'SP_IGNORE' } } },
-    },
-    Color = AutoColors.background_dark,
-	Raise_Arms = false,
-    Tweaks = {
-        impulse_strength = 15,
-        speed = 5,
-        foot_move_impulse = 12.5,
-        hip_move_impulse = 7.5,
-        orientation_randomness_scale = 0.35,
-        orientation_change_interval = 0.125,
-        step_interval = 0.4,
-        bite_interval = 0.65,
-        bite_damage = 1 / 3,
-        focus_end_distance = 0.65,
-        checkpoint_distance = 0.5,
-        focus_give_up_time = 4,
-        eye_half_fov = 55,
-        tag_on_unlink = 'SP_IGNORE'
-    },
-    Sounds = {
-        crunch = { LoadSound, 'masonry/hit-l0.ogg', 6 },
-        damage = { LoadSound, 'masonry/break-s0', 6 },
-        whine = false,
-        death = { LoadSound, 'masonry/break-m0', 15 },
-        step = false,
-    }
-}+#version 2

```

---

# Migration Report: script\Zspec\loose.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zspec\loose.lua
+++ patched/script\Zspec\loose.lua
@@ -1,45 +1 @@
-Zinject 'script/Automatic.lua'
-Zinject 'script/Zspec/default.lua'
-
-PROFILE = {
-    Weights = {
-        Chest =             { impulse = 1, 		apply_tags = { { 'autobreak' }, } },
-        Head =              { impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        ArmLeft =           { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        HandLeft =          { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        ArmRight =          { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        HandRight =         { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        Hips =              { impulse = 1.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegLeftUpper =      { impulse = 1.25, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegLeftLower =      { impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        FootLeft =			{ impulse = 0.75, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegRightUpper =		{ impulse = 1.25, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegRightLower =		{ impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        FootRight =			{ impulse = 0.75, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-    },
-    Color = AutoColors.green_light,
-	Raise_Arms = true,
-    Tweaks = {
-        impulse_strength = 17.5,
-        speed = 7.5,
-        foot_move_impulse = 25,
-        hip_move_impulse = 5,
-        orientation_randomness_scale = 0.65,
-        orientation_change_interval = 0.1,
-        step_interval = 0.25,
-        bite_interval = 0.55,
-        bite_damage = 1 / 3,
-        focus_end_distance = 0.65,
-        checkpoint_distance = 0.5,
-        focus_give_up_time = 4,
-        eye_half_fov = 55,
-        tag_on_unlink = 'SP_IGNORE'
-    },
-    Sounds = {
-        crunch = { LoadSound, 'MOD/snd/crunch-0.ogg', 6 },
-        damage = { LoadSound, 'MOD/snd/growl-0.ogg', 8 },
-        whine = { LoadLoop, 'MOD/snd/whine.ogg', 7 },
-        death = { LoadSound, 'MOD/snd/growl-0.ogg', 8 },
-        step = false,
-    }
-}+#version 2

```

---

# Migration Report: script\Zspec\marble.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zspec\marble.lua
+++ patched/script\Zspec\marble.lua
@@ -1,49 +1,4 @@
-Zinject 'script/Automatic.lua'
-Zinject 'script/Zspec/default.lua'
-
-PROFILE = {
-    Weights = {
-        Chest =             { impulse = 1, 		apply_tags = { } },
-        Head =              { impulse = 1.25, 	apply_tags = { } },
-        ArmLeft =           { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        HandLeft =          { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        ArmRight =          { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        HandRight =         { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        Hips =              { impulse = 1.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegLeftUpper =      { impulse = 1.25, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegLeftLower =      { impulse = 1.25, 	apply_tags = { } },
-        FootLeft =			{ impulse = 0.75, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegRightUpper =		{ impulse = 1.25, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegRightLower =		{ impulse = 1.25, 	apply_tags = { } },
-        FootRight =			{ impulse = 0.75, 	apply_tags = { { 'SP_IGNORE' } } },
-    },
-    Color = AutoColors.white,
-	Raise_Arms = true,
-    Tweaks = {
-        impulse_strength = 60,
-        speed = 5,
-        foot_move_impulse = 30,
-        hip_move_impulse = 20,
-        orientation_randomness_scale = 0.35,
-        orientation_change_interval = 0.125,
-        step_interval = 0.4,
-        bite_interval = 0.65,
-        bite_damage = 1 / 2,
-        focus_end_distance = 0.65,
-        checkpoint_distance = 0.5,
-        focus_give_up_time = 4,
-        eye_half_fov = 55,
-        tag_on_unlink = 'SP_IGNORE'
-    },
-    Sounds = {
-        crunch = { LoadSound, 'masonry/hit-s0.ogg', 6 },
-        damage = { LoadSound, 'masonry/break-m0', 6 },
-        whine = false,
-        death = { LoadSound, 'masonry/break-l0', 15 },
-        step = false,
-    }
-}
-
+#version 2
 function OVERRIDE_DAMAGE(damaged_shape_handle, damaged_shape_data, voxels_removed)
     local center = AutoShapeCenter(damaged_shape_handle)
 
@@ -73,4 +28,5 @@
     end
         
     Z.Mem.damage_LT = GetTime()
-end+end
+

```

---

# Migration Report: script\Zspec\pepper.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zspec\pepper.lua
+++ patched/script\Zspec\pepper.lua
@@ -1,49 +1,4 @@
-Zinject 'script/Automatic.lua'
-Zinject 'script/Zspec/default.lua'
-
-PROFILE = {
-    Weights = {
-        Chest =             { impulse = 1, 		apply_tags = { { 'autobreak' }, } },
-        Head =              { impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        ArmLeft =           { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        HandLeft =          { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        ArmRight =          { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        HandRight =         { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        Hips =              { impulse = 1.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegLeftUpper =      { impulse = 1.25, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegLeftLower =      { impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        FootLeft =			{ impulse = 0.75, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegRightUpper =		{ impulse = 1.25, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegRightLower =		{ impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        FootRight =			{ impulse = 0.75, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-    },
-    Color = AutoColors.green_light,
-	Raise_Arms = true,
-    Tweaks = {
-        impulse_strength = 20,
-        speed = 7.5,
-        foot_move_impulse = 25,
-        hip_move_impulse = 5,
-        orientation_randomness_scale = 0.75,
-        orientation_change_interval = 0.115,
-        step_interval = 0.2875,
-        bite_interval = 0.55,
-        bite_damage = 1 / 3,
-        focus_end_distance = 0.65,
-        checkpoint_distance = 0.5,
-        focus_give_up_time = 4,
-        eye_half_fov = 55,
-        tag_on_unlink = 'SP_IGNORE'
-    },
-    Sounds = {
-        crunch = { LoadSound, 'MOD/snd/crunch-0.ogg', 6 },
-        damage = { LoadSound, 'MOD/snd/growl-0.ogg', 8 },
-        whine = { LoadLoop, 'MOD/snd/whine.ogg', 7 },
-        death = { LoadSound, 'MOD/snd/anticipation_beep.ogg', 12 },
-        step = false,
-    }
-}
-
+#version 2
 local death_time = false
 local fuse_rel_transform
 
@@ -84,4 +39,5 @@
     end
     
     HandleBiting(1 / 3, 2 / 3)
-end+end
+

```

---

# Migration Report: script\Zspec\robot.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zspec\robot.lua
+++ patched/script\Zspec\robot.lua
@@ -1,45 +1 @@
-Zinject 'script/Automatic.lua'
-Zinject 'script/Zspec/default.lua'
-
-PROFILE = {
-    Weights = {
-        Chest =             { impulse = 1, 		apply_tags = { } },
-        Head =              { impulse = 1.25, 	apply_tags = { } },
-        ArmLeft =           { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        HandLeft =          { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        ArmRight =          { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        HandRight =         { impulse = 0.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        Hips =              { impulse = 1.5, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegLeftUpper =      { impulse = 1.25, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegLeftLower =      { impulse = 1.25, 	apply_tags = { } },
-        FootLeft =			{ impulse = 0.75, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegRightUpper =		{ impulse = 1.25, 	apply_tags = { { 'SP_IGNORE' } } },
-        LegRightLower =		{ impulse = 1.25, 	apply_tags = { } },
-        FootRight =			{ impulse = 0.75, 	apply_tags = { { 'SP_IGNORE' } } },
-    },
-    Color = AutoColors.green_light,
-	Raise_Arms = true,
-    Tweaks = {
-        impulse_strength = 80,
-        speed = 7.5,
-        foot_move_impulse = 30,
-        hip_move_impulse = 15,
-        orientation_randomness_scale = 0.75,
-        orientation_change_interval = 0.1,
-        step_interval = 0.25,
-        bite_interval = 0.55,
-        bite_damage = 1 / 3,
-        focus_end_distance = 0.65,
-        checkpoint_distance = 0.5,
-        focus_give_up_time = 4,
-        eye_half_fov = 55,
-        tag_on_unlink = 'SP_IGNORE'
-    },
-    Sounds = {
-        crunch = { LoadSound, 'spark0.ogg', 6 },
-        damage = { LoadSound, 'MOD/snd/growl-0.ogg', 8 },
-        whine = { LoadLoop, 'transmission.ogg', 12 },
-        death = { LoadSound, 'robot/hunt.ogg', 15 },
-        step = false,
-    }
-}+#version 2

```

---

# Migration Report: script\Zspec\strawberry.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zspec\strawberry.lua
+++ patched/script\Zspec\strawberry.lua
@@ -1,45 +1 @@
-Zinject 'script/Automatic.lua'
-Zinject 'script/Zspec/default.lua'
-
-PROFILE = {
-    Weights = {
-        Chest =             { impulse = 1, 		apply_tags = { { 'autobreak' }, } },
-        Head =              { impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        ArmLeft =           { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        HandLeft =          { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        ArmRight =          { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        HandRight =         { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        Hips =              { impulse = 1.75, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegLeftUpper =      { impulse = 1.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegLeftLower =      { impulse = 1.5, 	apply_tags = { { 'autobreak' }, } },
-        FootLeft =			{ impulse = 0.75, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegRightUpper =		{ impulse = 1.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegRightLower =		{ impulse = 1.5, 	apply_tags = { { 'autobreak' }, } },
-        FootRight =			{ impulse = 0.75, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-    },
-    Color = AutoColors.green_light,
-	Raise_Arms = true,
-    Tweaks = {
-        impulse_strength = 17.5,
-        speed = 8,
-        foot_move_impulse = 35,
-        hip_move_impulse = 30,
-        orientation_randomness_scale = 0.75,
-        orientation_change_interval = 0.067,
-        step_interval = 0.2,
-        bite_interval = 0.55,
-        bite_damage = 1 / 3,
-        focus_end_distance = 0.85,
-        checkpoint_distance = 0.5,
-        focus_give_up_time = 4,
-        eye_half_fov = 55,
-        tag_on_unlink = 'SP_IGNORE'
-    },
-    Sounds = {
-        crunch = { LoadSound, 'MOD/snd/crunch-0.ogg', 6 },
-        damage = { LoadSound, 'MOD/snd/growl-0.ogg', 8 },
-        whine = { LoadLoop, 'MOD/snd/whine.ogg', 7 },
-        death = { LoadSound, 'MOD/snd/growl-0.ogg', 8 },
-        step = false,
-    }
-}+#version 2

```

---

# Migration Report: script\Zspec\tvstatic.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zspec\tvstatic.lua
+++ patched/script\Zspec\tvstatic.lua
@@ -1,52 +1,7 @@
-Zinject 'script/Automatic.lua'
-Zinject 'script/Zspec/default.lua'
+#version 2
+local noise_sprites = { LoadSprite('MOD/assets/noise0.png'), LoadSprite('MOD/assets/noise1.png'), LoadSprite('MOD/assets/noise2.png'), LoadSprite('MOD/assets/noise3.png') }
+local death_time = false
 
-PROFILE = {
-    Weights = {
-        Chest =             { impulse = 1, 		apply_tags = { { 'autobreak' }, } },
-        Head =              { impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        ArmLeft =           { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        HandLeft =          { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        ArmRight =          { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        HandRight =         { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        Hips =              { impulse = 1.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegLeftUpper =      { impulse = 1.25, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegLeftLower =      { impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        FootLeft =			{ impulse = 0.75, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegRightUpper =		{ impulse = 1.25, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegRightLower =		{ impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        FootRight =			{ impulse = 0.75, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-    },
-    Color = AutoColors.green_light,
-	Raise_Arms = true,
-    Tweaks = {
-        impulse_strength = 20,
-        speed = 7.5,
-        foot_move_impulse = 25,
-        hip_move_impulse = 5,
-        orientation_randomness_scale = 0.75,
-        orientation_change_interval = 0.1,
-        step_interval = 0.25,
-        bite_interval = 0.55,
-        bite_damage = 1 / 3,
-        focus_end_distance = 0.65,
-        checkpoint_distance = 0.5,
-        focus_give_up_time = 4,
-        eye_half_fov = 55,
-        tag_on_unlink = 'SP_IGNORE'
-    },
-    Sounds = {
-        crunch = { LoadSound, 'tools/snowball0.ogg', 6 },
-        damage = { LoadSound, 'MOD/snd/glitch-0.ogg.ogg', 8 },
-        whine = { LoadLoop, 'MOD/snd/tvstatic.ogg', 4 },
-        death = { LoadSound, 'robot/step-l0', 15 },
-        step = false,
-    }
-}
-
-local noise_sprites = { LoadSprite('MOD/assets/noise0.png'), LoadSprite('MOD/assets/noise1.png'), LoadSprite('MOD/assets/noise2.png'), LoadSprite('MOD/assets/noise3.png') }
-
-local death_time = false
 function OVERRIDE_DEATH()
     death_time = GetTime()
 end
@@ -99,7 +54,7 @@
         f.rot = QuatRotateQuat(f.rot, QuatEuler(0, 0, math.random(0, 1) * 180))
 
         local dot = VecDot(VecSub(f.pos, camera.pos), forward)
-        if dot > 0 then
+        if dot ~= 0 then
             if Z.Mem.seen_by_player then
                 local c = AutoColors.green_light
                 AutoDrawPlane(f, 0, 0, false, c[1], c[2], c[3], 1, TVLine)
@@ -118,8 +73,3 @@
     end
 end
 
--- function OVVERIDE_DEATH()
---     for handle, data in pairs(Z.shape_data) do
---         RemoveTag(handle, 'invisible')
---     end
--- end
```

---

# Migration Report: script\Zspec\void.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Zspec\void.lua
+++ patched/script\Zspec\void.lua
@@ -1,51 +1,11 @@
-Zinject 'script/Automatic.lua'
-Zinject 'script/Zspec/default.lua'
-
-PROFILE = {
-    Weights = {
-        Chest =             { impulse = 1, 		apply_tags = { { 'autobreak' }, } },
-        Head =              { impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        ArmLeft =           { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        HandLeft =          { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        ArmRight =          { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        HandRight =         { impulse = 0.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        Hips =              { impulse = 1.5, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegLeftUpper =      { impulse = 1.25, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegLeftLower =      { impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        FootLeft =			{ impulse = 0.75, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegRightUpper =		{ impulse = 1.25, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-        LegRightLower =		{ impulse = 1.25, 	apply_tags = { { 'autobreak' }, } },
-        FootRight =			{ impulse = 0.75, 	apply_tags = { { 'autobreak' }, { 'SP_IGNORE' } } },
-    },
-    Color = AutoColors.green_light,
-	Raise_Arms = true,
-    Tweaks = {
-        impulse_strength = 20,
-        speed = 7.5,
-        foot_move_impulse = 10,
-        hip_move_impulse = 10,
-        orientation_randomness_scale = 0.6,
-        orientation_change_interval = 0.1,
-        step_interval = 0.25,
-        focus_end_distance = 0.65,
-        checkpoint_distance = 1,
-        focus_give_up_time = 4,
-        eye_half_fov = 55,
-        tag_on_unlink = 'SP_IGNORE'
-    },
-    Sounds = {
-        damage = { LoadSound, 'MOD/snd/glitch-0.ogg', 8 },
-        whine = { LoadLoop, 'MOD/snd/soup.ogg', 10 },
-        -- whine = { LoadLoop, 'radio/credits.ogg', 10 },
-        death = { LoadSound, 'silenced0.ogg', 8 },
-        step = false,
-    }
-}
-
+#version 2
 local snd = {
     bite = LoadSound('MOD/snd/void-bite.ogg', 20),
     loop = LoadLoop('MOD/snd/void-loop.ogg', 20),
 }
+local bite_lt = -1 / 0
+local bit = false
+local clone_env = false
 
 local function ParticleLine(p1, p2, r, g, b)
     ParticleReset()
@@ -66,7 +26,6 @@
     end
 end
 
-
 function CB_SHAPE_LOOP_TICK(handle, data, dt)
     DrawShapeHighlight(handle, -1 / 0)
 
@@ -79,7 +38,7 @@
         f.rot = QuatRotateQuat(f.rot, QuatEuler(0, 0, math.random(0, 1) * 180))
 
         local dot = VecDot(VecSub(f.pos, camera.pos), forward)
-        if dot > 0 then
+        if dot ~= 0 then
             local c = ((1 - math.max(dot, 0)) / 2) ^ 0.5
             local half_size_increase = 0.025
             DrawSprite(AutoFlatSprite,
@@ -110,18 +69,14 @@
     end
 end
 
-local bite_lt = -1 / 0
-local bit = false
-local clone_env = false
-
 function HandleBiting()
 	local Time = GetTime()
-	local player = GetPlayerTransform()
+	local player = GetPlayerTransform(playerId)
 
     if bit then return end
     
 	-------------------------------- Bite --------------------------------
-	if Time - bite_lt > 2 / 3 and GetPlayerVehicle() == 0 then
+	if Time - bite_lt > 2 / 3 and GetPlayerVehicle(playerId) == 0 then
 		if AutoVecDist(Z.Mem.center, VecAdd(player.pos, Vec(0, 1.8/2))) < 0.65 then
 			PlaySound(snd.bite, Z.Mem.center, 2)
             ShakeCamera(2)
@@ -141,9 +96,9 @@
     HandleBiting()
 
     if bit then
-        SetBool('game.disablepause', true)
-        SetBool('game.disablemap', true)
-        SetBool('hud.disable', true)
+        SetBool('game.disablepause', true, true)
+        SetBool('game.disablemap', true, true)
+        SetBool('hud.disable', true, true)
         local camera = GetCameraTransform()
 
         ShakeCamera(0.15)
@@ -154,8 +109,8 @@
             PlaySound(Z.Sounds.damage, Z.Mem.center, 2)
         end
 
-        local new_health = GetPlayerHealth() - dt * 0.2
-        SetPlayerHealth(new_health)
+        local new_health = GetPlayerHealth(playerId) - dt * 0.2
+        SetPlayerHealth(playerId, new_health)
 
         if new_health < 0 then
             SetTag(Z.script, 'status', 'dead')
@@ -183,4 +138,5 @@
     if bit then
         AutoSetEnvironment(clone_env)
     end
-end+end
+

```
