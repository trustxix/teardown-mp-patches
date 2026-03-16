# Migration Report: Automatic.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Automatic.lua
+++ patched/Automatic.lua
@@ -1,50 +1,76 @@
--- VERSION 3.09
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
@@ -1165,15 +840,6 @@
 	end
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
@@ -1213,7 +879,7 @@
 			linefunction(subH1, subH2, r, g, b, a)
 			linefunction(subV1, subV2, r, g, b, a)
 		end
-	elseif pattern > 0 then
+	elseif pattern ~= 0 then
 		linefunction(corner1, corner2, r, g, b, a)
 		linefunction(corner2, corner3, r, g, b, a)
 		linefunction(corner3, corner4, r, g, b, a)
@@ -1248,16 +914,6 @@
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
@@ -1284,11 +940,6 @@
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
@@ -1297,10 +948,6 @@
 	return hit, { pos = point, normal = normal, shape }
 end
 
----Draws the Octree from AutoProcessOctree
----@param node table
----@param layer number
----@param drawfunction function?
 function AutoDrawOctree(node, layer, drawfunction)
 	if node == nil then return end
 	
@@ -1324,10 +971,6 @@
 	end
 end
 
---#endregion
---#region Point Physics
-
----Creates a Point Physics Simulation Instance
 function AutoSimInstance()
 	local t = {
 		Points = {
@@ -1498,21 +1141,6 @@
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
@@ -1544,13 +1172,6 @@
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
@@ -1569,11 +1190,6 @@
 	return sosdata
 end
 
----Updates the state of the Second Order System (SOS) towards the target value, over the specified timestep.
----This function is used in conjunction with the AutoSM_Define
----@param sm Secondary_Motion_Data
----@param target number|table<number>
----@param timestep number?
 function AutoSM_Update(sm, target, timestep)
 	timestep = timestep or GetTimeStep()
 	
@@ -1619,9 +1235,6 @@
 	end
 end
 
----Returns the current value of a Second Order System
----@param sm Secondary_Motion_Data
----@return number|table<number>|quaternion
 function AutoSM_Get(sm)
 	if sm.type ~= 'table' then
 		return sm.data.current
@@ -1635,9 +1248,6 @@
 	end
 end
 
----Returns the current velocity of a Second Order System
----@param sm Secondary_Motion_Data
----@return number|table<number>
 function AutoSM_GetVelocity(sm)
 	if sm.type ~= 'table' then
 		return sm.data.velocity
@@ -1646,10 +1256,6 @@
 	end
 end
 
----Sets the current values of a Second Order System
----@param sm Secondary_Motion_Data
----@param target number|table<number>|quaternion
----@param keep_velocity boolean?
 function AutoSM_Set(sm, target, keep_velocity)
 	if sm.type ~= 'table' then
 		sm.data.current = target
@@ -1670,9 +1276,6 @@
 	end
 end
 
----Sets the current velocity of a Second Order System
----@param sm Secondary_Motion_Data
----@param velocity number|table<number>
 function AutoSM_SetVelocity(sm, velocity)
 	if sm.type == 'single' then
 		sm.data.velocity = velocity
@@ -1685,9 +1288,6 @@
 	end
 end
 
----Adds a amount to the current velocity of a Second Order System
----@param sm Secondary_Motion_Data
----@param velocity number|table<number>
 function AutoSM_AddVelocity(sm, velocity)
 	if sm.type == 'single' then
 		sm.data.velocity = sm.data.velocity + velocity
@@ -1700,12 +1300,6 @@
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
@@ -1714,12 +1308,6 @@
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
@@ -1729,10 +1317,6 @@
 	return c
 end
 
----Repeats a value `v`, `r` amount of times
----@param v any
----@param r integer
----@return table
 function AutoTableRepeatValue(v, r)
 	local t = {}
 	for i=1,r do
@@ -1741,18 +1325,12 @@
 	return t
 end
 
----Concats Table 2 onto the end of Table 1, does not return anything
----@param t1 table
----@param t2 table
 function AutoTableConcat(t1, t2)
 	for i = 1, #t2 do
 		t1[#t1 + 1] = t2[i]
 	end
 end
 
----Merges two tables together, does not return anything
----@param base table
----@param overwrite table
 function AutoTableMerge(base, overwrite)
 	for k, v in pairs(overwrite) do
 		if type(v) == "table" then
@@ -1767,10 +1345,6 @@
 	end
 end
 
----A lambda like function for returning a table's key's values.
----@param t table
----@param key any
----@return table
 function AutoTableSub(t, key)
 	local _t = {}
 	for i, v in pairs(t) do
@@ -1779,11 +1353,6 @@
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
@@ -1792,9 +1361,6 @@
 	return _t
 end
 
----Swaps the keys and the values of a table
----@param t table
----@return table
 function AutoTableSwapKeysAndValues(t)
 	local _t = {}
 	for k, v in pairs(t) do
@@ -1803,25 +1369,12 @@
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
@@ -1831,18 +1384,10 @@
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
@@ -1864,20 +1409,10 @@
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
 	
@@ -1892,11 +1427,6 @@
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
@@ -1905,11 +1435,6 @@
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
@@ -1918,12 +1443,6 @@
 	return c
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
@@ -1934,58 +1453,31 @@
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
@@ -1997,19 +1489,11 @@
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
 	
@@ -2032,11 +1516,6 @@
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
@@ -2061,9 +1540,6 @@
 	return h, s, v
 end
 
----Converts a hex code or a table of hex codes to RGB color space
----@param hex string|table<string>
----@return number|table
 function AutoHEXtoRGB(hex)
 	local function f(x, p)
 		x = x:gsub("#", "")
@@ -2081,11 +1557,6 @@
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
@@ -2105,9 +1576,6 @@
 	end
 end
 
----Performs `:byte()` on each character of a given string
----@param str string
----@return table<number>
 function AutoStringToByteTable(str)
 	local t = {}
 	for i = 1, #str do
@@ -2116,11 +1584,6 @@
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
@@ -2129,18 +1592,12 @@
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
@@ -2148,10 +1605,6 @@
 	return value
 end
 
----Goes through a table and performs Delete() on each element
----@param t table<entity_handle>
----@param CheckIfValid boolean?
----@return table<{handle:entity_handle, type:entity_type, valid:boolean}>
 function AutoDeleteHandles(t, CheckIfValid)
 	local list = {}
 	for k, v in pairs(t) do
@@ -2175,10 +1628,6 @@
 	return T
 end
 
-
----Creates a list from a table of entity handles, containing the handle and it's type. If the handle is invalid then the type will be false.
----@param t table<entity_handle>
----@return table<{handle:entity_handle, type:entity_type}>
 function AutoListHandleTypes(t)
 	local nt = {}
 	for key, value in pairs(t) do
@@ -2187,21 +1636,12 @@
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
 
----Attempts to get the handle of the current script by abusing pause menu item keys
----
----May not work if a pause menu button is already being created from the script
----
----Original coded from Thomasims
 function AutoGetScriptHandle()
 	local id = tostring(math.random())
 	PauseMenuButton(id)
@@ -2212,13 +1652,6 @@
 	end
 end
 
----A Wrapper for QueryRaycast; comes with some extra features.
----@param origin vector
----@param direction vector
----@param maxDist number
----@param radius number?
----@param rejectTransparent boolean?
----@return { hit:boolean, intersection:vector, dist:number, normal:vector, shape:shape_handle, body:body_handle, dot:number, reflection:vector }
 function AutoRaycast(origin, direction, maxDist, radius, rejectTransparent)
 	direction = direction and VecNormalize(direction) or nil
 	
@@ -2232,37 +1665,18 @@
 	return data
 end
 
----AutoRaycast from point A to point B. The distance will default to the distance between the points, but can be set.
----@param pointA vector
----@param pointB vector
----@param manualDistance number?
----@param radius number?
----@param rejectTransparent boolean?
----@return { hit:boolean, dist:number, normal:vector, shape:shape_handle, intersection:vector, body:body_handle, dot:number, reflection:vector }
 function AutoRaycastTo(pointA, pointB, manualDistance, radius, rejectTransparent)
 	local diff = VecSub(pointB, pointA)
 	return AutoRaycast(pointA, diff, manualDistance or VecLength(diff), radius, rejectTransparent)
 end
 
----AutoRaycast using the camera or player camera as the origin and direction
----@param usePlayerCamera boolean
----@param maxDist number
----@param radius number?
----@param rejectTransparent boolean?
----@return { hit:boolean, dist:number, normal:vector, shape:shape_handle, intersection:vector, body:body_handle, dot:number, reflection:vector }
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
@@ -2284,10 +1698,6 @@
 	return data
 end
 
----A Wrapper for GetBodyClosestPoint; comes with some extra features.
----@param body body_handle
----@param origin vector
----@return { hit:boolean, point:vector, normal:vector, shape:shape_handle, body:body_handle, dist:number, dir:vector, dot:number, reflection:vector }
 function AutoQueryClosestBody(body, origin)
 	local data = {}
 	data.hit, data.point, data.normal, data.shape = GetBodyClosestPoint(body, origin)
@@ -2307,10 +1717,6 @@
 	return data
 end
 
----A Wrapper for GetShapeClosestPoint; comes with some extra features.
----@param shape shape_handle
----@param origin vector
----@return { hit:boolean, point:vector, normal:vector, dist:number, dir:vector, dot:number, reflection:vector }
 function AutoQueryClosestShape(shape, origin)
 	local data = {}
 	data.hit, data.point, data.normal = GetShapeClosestPoint(shape, origin)
@@ -2329,9 +1735,6 @@
 	return data
 end
 
----Goes through each shape on a body and adds up their voxel count
----@param body body_handle
----@return integer
 function AutoGetBodyVoxels(body)
 	local v = 0
 	for _, s in pairs(GetBodyShapes(body)) do
@@ -2340,11 +1743,6 @@
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
@@ -2352,11 +1750,6 @@
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
@@ -2364,10 +1757,6 @@
 	return scaled, current
 end
 
----Gets the angle from a point to the forward direction of a transform
----@param point vector
----@param fromtrans transform
----@return number
 function AutoPointToAngle(point, fromtrans)
 	fromtrans = AutoDefault(fromtrans, GetCameraTransform())
 	
@@ -2378,14 +1767,6 @@
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
@@ -2409,7 +1790,7 @@
 		if raycastcheck then
 			local hit, hitdist = QueryRaycast(oftrans.pos, fromtopointdir, dist, 0, true)
 			if hit then
-				if raycasterror > 0 then
+				if raycasterror ~= 0 then
 					local hitpoint = VecAdd(oftrans.pos, VecScale(fromtopointdir, hitdist))
 					if AutoVecDist(hitpoint, point) > raycasterror then
 						seen = false
@@ -2424,11 +1805,6 @@
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
@@ -2437,10 +1813,6 @@
 	}, length or 1)
 end
 
----Get the last Path Query as a path of points
----@param precision number The Accuracy
----@return table<vector>
----@return vector "Last Point"
 function AutoRetrievePath(precision)
 	precision = AutoDefault(precision, 0.2)
 	
@@ -2455,8 +1827,6 @@
 	return path, path[#path]
 end
 
----Reject a table of bodies for the next Query
----@param bodies table<body_handle>
 function AutoQueryRejectBodies(bodies)
 	for _, h in pairs(bodies) do
 		if h then
@@ -2465,8 +1835,6 @@
 	end
 end
 
----Reject a table of shapes for the next Query
----@param shapes table<shape_handle>
 function AutoQueryRejectShapes(shapes)
 	for _, h in pairs(shapes) do
 		if h then
@@ -2475,8 +1843,6 @@
 	end
 end
 
----Finds and rejects all shapes that do not have a given tag
----@param tag string
 function AutoRejectShapesWithoutTag(tag)
 	local all = FindShapes(nil, true)
 	local keep = {}
@@ -2489,10 +1855,6 @@
 	end
 end
 
----Set the collision filter for the shapes owned by a body
----@param body body_handle
----@param layer number
----@param masknummber number bitmask
 function AutoSetBodyCollisionFilter(body, layer, masknummber)
 	local shapes = GetBodyShapes(body)
 	for i in pairs(shapes) do
@@ -2500,30 +1862,16 @@
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
@@ -2557,17 +1905,11 @@
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
 	
@@ -2588,46 +1930,6 @@
 	return log, vel, normal
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
 		"ambience",
@@ -2671,8 +1973,6 @@
 	return assembled
 end
 
----Sets every environment property of AutoGetEnvironment
----@param Environment environment
 function AutoSetEnvironment(Environment)
 	for k, v in pairs(Environment) do
 		if type(v) == "table" then
@@ -2685,12 +1985,6 @@
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
@@ -2716,11 +2010,6 @@
 end
 end
 
----Returns and environemnt that eliminates as much lighting as possible, making colors look flat.
----
----Requires a flat DDS file.
----@param pathToDDS td_path
----@return table
 function AutoFlatEnvironment(pathToDDS)
 	return {
 		ambience = { "outdoor/field.ogg", 0 },
@@ -2757,18 +2046,6 @@
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
@@ -2786,8 +2063,6 @@
 	return assembled
 end
 
----Sets every post-processing property of AutoGetPostProcessing
----@param PostProcessing postprocessing
 function AutoSetPostProcessing(PostProcessing)
 	
 	for k, v in pairs(PostProcessing) do
@@ -2801,45 +2076,18 @@
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
@@ -2889,14 +2137,6 @@
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
@@ -2911,44 +2151,20 @@
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
@@ -2982,15 +2198,6 @@
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
@@ -2998,13 +2205,6 @@
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
@@ -3046,15 +2246,6 @@
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
@@ -3068,12 +2259,6 @@
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
@@ -3095,13 +2280,6 @@
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
@@ -3155,26 +2333,17 @@
 AutoHandleSpread(AutoGetSpread(), data, 'draw')
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
@@ -3191,137 +2360,46 @@
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
@@ -3330,30 +2408,16 @@
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
@@ -3368,12 +2432,6 @@
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
@@ -3397,13 +2455,6 @@
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
@@ -3413,7 +2464,7 @@
 	
 	UiPush()
 	
-	if radius > 0 then
+	if radius ~= 0 then
 		UiPush()
 		UiTranslate(unpack(p1))
 		AutoUiCircle(radius, line_width, 32)
@@ -3438,13 +2489,6 @@
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
@@ -3454,477 +2498,6 @@
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
@@ -3938,21 +2511,13 @@
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
@@ -3973,4 +2538,3 @@
 	return results
 end
 
---#endregion
```

---

# Migration Report: avf\prefabs\ZSU_23_4\ZSU-23-4.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\ZSU_23_4\ZSU-23-4.lua
+++ patched/avf\prefabs\ZSU_23_4\ZSU-23-4.lua
@@ -1,131 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {
-					
-					name = "23 mm 2A7 autocannons",
-					weaponType 				= "cannon",
-					caliber 				= 23,
-					default = "B_23mm_AA",
-					magazines 					= 
-					{
-						[1] = {
-								name= "B_23mm_AA",
-								magazineCapacity = 200,
-								ammoCount = 0,
-								magazineCount = 30,
-								caliber 				= 23,
-								velocity				= 220,
-								explosionSize 			= .6,
-								maxPenDepth 			= 0.1,
-								timeToLive 				= 7,
-								launcher				= "cannon",
-								payload					= "HE",
-								shellWidth				= 0.1,
-								shellHeight				= 0.7,
-								r						= 0.5,
-								g						= 0.5, 
-								b						= 0.5, 
-								tracer 					= 1,
-								tracerL					= 5,
-								tracerW					= 2,
-								tracerR					= 1.8,
-								tracerG					= 1.0, 
-								tracerB					= 1.0, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-							},
-						[2] = {
-								name= "B_23mm_AA_AP",
-								magazineCapacity = 200,
-								ammoCount = 0,
-								magazineCount = 30,
-								caliber 				= 23,
-								velocity				= 220,
-								explosionSize 			= .6,
-								maxPenDepth 			= 0.5,
-								timeToLive 				= 7,
-								launcher				= "cannon",
-								payload					= "AP",
-								shellWidth				= 0.1,
-								shellHeight				= 0.7,
-								r						= 0.5,
-								g						= 0.5, 
-								b						= 0.5, 
-								tracer 					= 1,
-								tracerL					= 5,
-								tracerW					= 2,
-								tracerR					= 1.8,
-								tracerG					= 1.0, 
-								tracerB					= 1.0, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-							},
-
-					},
-					loadedMagazine 			= 1,
-					barrels = 
-								{
-									[1] = {x=.6,y=.6,z=-1.0},
-									[2] = {x=0.2,y=.1,z=-1.0},
-									[3] = {x=.2,y=.6,z=-1.0},
-									[4] = {x=0.6,y=.1,z=-1.0},
-								},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 3,
-												y = 1.3,
-												z = 0.3,
-											},
-
-
-												},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/zsuDUBLAR2.png",
-					highVelocityShells		= true,
-					RPM 					= 700,
-					reload 					= 4,
-					recoil 					= 0.2,
-					dispersion 				= 10,
-					gunRange				= 500,
-					gunBias 				= -1,
-					smokeFactor 			= .3,
-					smokeMulti				= 1,
-					soundFile   = "MOD/sounds/zsuSingle",
-					mouseDownSoundFile 		=	"MOD/sounds/zsuMulti0",
-					loopSoundFile 			=	"MOD/sounds/zsuFiring_long-2.ogg",
-					tailOffSound	 		=	"MOD/sounds/zsuSingle",
-
-
-		},
-
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: demo\nocull.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/demo\nocull.lua
+++ patched/demo\nocull.lua
@@ -1,5 +1,7 @@
-function init()
+#version 2
+function server.init()
     for index, s in ipairs(FindShapes('', true)) do
         SetTag(s, 'nocull')
     end
 end
+

```

---

# Migration Report: levelLoader.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/levelLoader.lua
+++ patched/levelLoader.lua
@@ -1,89 +1,4 @@
-#include "script.lua"
-
-function init()
-
-    CheckRegInitialized()
-
-    Init_Config()
-
-    if GetBool('savegame.mod.debugMode') then
-        if GetBool('savegame.mod.testMap') then
-            StartLevel('', 'test.xml', '')
-        else
-            StartLevel('', 'demo.xml', '')
-        end
-    end
-
-    ui = {
-        text = {
-            size = {
-                s = 24,
-                m = 48,
-                l = 64,
-            },
-        },
-    }
-
-    Pad = 10
-    Pad2 = Pad*2
-
-end
-
-function tick()
-
-    -- if InputPressed("g") then
-    --     ClearKey("savegame.mod")
-    --     print("Reset reg level loader...")
-    -- end
-
-    if GetBool('savegame.mod.debugMode') then
-        if GetBool('savegame.mod.testMap') then
-            StartLevel('', 'test.xml', '')
-        else
-            StartLevel('', 'demo.xml', '')
-        end
-    end
-
-    FlightMode = GetString("savegame.mod.FlightMode")
-    FlightModeSet = GetBool("savegame.mod.flightmodeset")
-
-    if InputPressed("pause") then
-        Menu()
-    end
-
-end
-
-
-function draw()
-
-    UiColor(0.6,0.6,0.6,1)
-    UiRect(UiWidth(), UiHeight())
-    UiMakeInteractive()
-
-    uiSetFont(ui.text.size.m)
-
-    UiPush()
-        draw_mainmenu_banner()
-
-        if not FlightModeSet then
-            draw_flightModeSelection()
-        else
-            draw_levelSelection()
-        end
-    UiPop()
-
-    UiColor(0,0,0, 1)
-    UiAlign("center bottom")
-    UiTranslate(UiCenter(), UiHeight() - 25)
-    UiButtonImageBox("ui/common/box-outline-6.png", 10,10, 0,0,0, 1)
-    if UiTextButton('Close', 150, 70) then
-        Menu()
-    end
-
-
-end
-
-
+#version 2
 function draw_mainmenu_banner(w, h)
     UiPush()
 
@@ -101,7 +16,6 @@
         UiImageBox("MOD/img/Preview.png", h,h, 0,0)
         UiTranslate(h+ Pad, 0)
 
-
         uiSetFont(ui.text.size.l)
         UiText("Flying Planes")
 
@@ -112,7 +26,6 @@
     UiPop()
 end
 
-
 function draw_flightModeSelection()
 
     do UiPush()
@@ -120,7 +33,6 @@
         UiColor(1,1,1,1)
         UiFont("regular.ttf",  48)
         UiAlign('center middle')
-
 
         UiTranslate(UiCenter(), UiMiddle()/2)
         UiColor(0,0,0,1)
@@ -140,8 +52,8 @@
 
             UiButtonImageBox("ui/common/box-outline-6.png", 10,10, 1,1,1, 1)
             if UiTextButton(' ', 500, 300) then
-                SetString("savegame.mod.FlightMode", "simple")
-                SetBool("savegame.mod.flightmodeset", true)
+                SetString("savegame.mod.FlightMode", "simple", true)
+                SetBool("savegame.mod.flightmodeset", true, true)
                 print("level loader: simple")
             end
         UiPop() end
@@ -160,18 +72,16 @@
 
             UiButtonImageBox("ui/common/box-outline-6.png", 10,10, 1,1,1, 1)
             if UiTextButton(' ', 500, 300) then
-                SetString("savegame.mod.FlightMode", "simulation")
-                SetBool("savegame.mod.flightmodeset", true)
+                SetString("savegame.mod.FlightMode", "simulation", true)
+                SetBool("savegame.mod.flightmodeset", true, true)
                 print("level loader: simulation")
             end
 
         UiPop() end
 
-
     UiPop() end
 
 end
-
 
 function draw_levelSelection()
 
@@ -217,7 +127,77 @@
 
         UiPop() end
 
-
     UiPop() end
 
 end
+
+function server.init()
+    CheckRegInitialized()
+    Init_Config()
+    if GetBool('savegame.mod.debugMode') then
+        if GetBool('savegame.mod.testMap') then
+            StartLevel('', 'test.xml', '')
+        else
+            StartLevel('', 'demo.xml', '')
+        end
+    end
+    ui = {
+        text = {
+            size = {
+                s = 24,
+                m = 48,
+                l = 64,
+            },
+        },
+    }
+    Pad = 10
+    Pad2 = Pad*2
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetBool('savegame.mod.debugMode') then
+            if GetBool('savegame.mod.testMap') then
+                StartLevel('', 'test.xml', '')
+            else
+                StartLevel('', 'demo.xml', '')
+            end
+        end
+        FlightMode = GetString("savegame.mod.FlightMode")
+        FlightModeSet = GetBool("savegame.mod.flightmodeset")
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("pause") then
+        Menu()
+    end
+end
+
+function client.draw()
+    UiColor(0.6,0.6,0.6,1)
+    UiRect(UiWidth(), UiHeight())
+    UiMakeInteractive()
+
+    uiSetFont(ui.text.size.m)
+
+    UiPush()
+        draw_mainmenu_banner()
+
+        if not FlightModeSet then
+            draw_flightModeSelection()
+        else
+            draw_levelSelection()
+        end
+    UiPop()
+
+    UiColor(0,0,0, 1)
+    UiAlign("center bottom")
+    UiTranslate(UiCenter(), UiHeight() - 25)
+    UiButtonImageBox("ui/common/box-outline-6.png", 10,10, 0,0,0, 1)
+    if UiTextButton('Close', 150, 70) then
+        Menu()
+    end
+end
+

```

---

# Migration Report: options.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/options.lua
+++ patched/options.lua
@@ -1,148 +1,4 @@
-#include "script.lua"
-#include "TDSU/tdsu.lua"
-#include "script/registry.lua"
-
-
-
-
-activeAssignment = false
-activePath = '.'
-lastKeyPressed = '.'
-font_size = 32
-
-
-function init()
-
-    CheckRegInitialized()
-
-    Init_Config()
-
-end
-
-function tick()
-
-    ManageUiBinding()
-
-    if activeAssignment and InputLastPressedKey() ~= '' then
-
-        SetString(activePath, string.lower(InputLastPressedKey()))
-        activeAssignment = false
-        activePath = ''
-
-    end
-
-end
-
-
-
-function draw()
-
-    UiColor(1,1,1,1)
-    UiFont('regular.ttf', font_size)
-    UiTranslate(UiCenter(), 0)
-
-    do UiPush()
-
-        -- Title
-        do UiPush()
-            UiTranslate(0, font_size)
-            UiFont('regular.ttf', 64)
-            UiAlign('center top')
-            UiText('Flying Planes')
-
-            UiTranslate(0, 64)
-            UiFont('regular.ttf', 32)
-            UiText('By: Cheejins')
-        UiPop() end
-
-
-        -- Button : Start Demo Map
-        do UiPush()
-
-            UiAlign('center middle')
-            UiFont('regular.ttf', font_size*1.5)
-            UiTranslate(0, 190)
-            -- local c = Oscillate(2)/3 + 2/3
-            -- UiColor(c,c,1,1)
-            -- UiButtonImageBox("ui/common/box-outline-6.png", 10,10)
-            -- UiButtonHoverColor(0.5,0.5,1,1)
-            -- if UiTextButton('Start Demo Map', 350, font_size*2.5) then
-            --     StartLevel('', 'demo.xml', '')
-            -- end
-
-            UiTranslate(0, 80)
-            UiColor(1,1,1,1)
-
-            UiTranslate(0, font_size*2.5)
-            Ui_Option_Keybind(250, font_size*2, 0, "Change Target", Config.changeTarget, Config, "changeTarget")
-
-            UiTranslate(0, font_size*2.5)
-            Ui_Option_Keybind(250, font_size*2, 0, "Toggle Missile Homing", Config.toggleHoming, Config, "toggleHoming")
-
-            UiFont('regular.ttf', 32)
-            UiTranslate(0, font_size*3)
-            UiText("More keybinds coming soon.")
-
-        UiPop() end
-
-
-    UiPop() end
-
-
-    do UiPush()
-
-        UiTranslate(0, UiHeight() - 150)
-
-        UiAlign('center middle')
-        UiButtonImageBox('ui/common/box-outline-6.png', 10,10, 1, 1, 1, 1)
-        if UiTextButton('Reset', 150, font_size*2) then
-            ClearKey("savegame.mod")
-        end
-
-        UiTranslate(0, font_size*2.5)
-
-        UiButtonImageBox("ui/common/box-outline-6.png", 10,10)
-        UiButtonHoverColor(0.5,0.5,1,1)
-        if UiTextButton('Close', 150, font_size*2) then
-            Menu()
-        end
-
-
-    UiPop() end
-
-end
-
-
--- function Ui_Option_Keybind(label, regPath)
-
---     do UiPush()
-
---         -- Label
---         UiFont('regular.ttf', font_size)
---         UiAlign('right middle')
---         UiTranslate(0, font_size)
---         UiText(label)
-
---         -- Bind button
---         UiTranslate(font_size, 0)
---         UiAlign('left middle')
---         UiButtonImageBox("ui/common/box-outline-6.png", 10,10)
---         UiButtonHoverColor(0.5,0.5,1,1)
---         if UiTextButton(GetString(regPath), font_size*6, font_size*2) then
-
---             if not activeAssignment then
---                 SetString(regPath, 'Press key...')
---                 activeAssignment = true
---                 activePath = regPath
---             end
-
---         end
-
---     UiPop() end
-
--- end
-
-
+#version 2
 function ui_createToggleSwitch(title, registryPath)
 
     do UiPush()
@@ -156,7 +12,6 @@
         UiFont('regular.ttf', font_size)
         UiText(title)
         UiTranslate(font_size, -font_size/2)
-
 
         -- Toggle BG
         UiAlign('left top')
@@ -192,7 +47,7 @@
 
         UiButtonImageBox('ui/common/box-outline-6.png', 10,10, 0,0,0, a)
         if UiBlankButton(tglW, tglH) then
-            SetBool(registryPath, not value)
+            SetBool(registryPath, not value, true)
             PlaySound(LoadSound('clickdown.ogg'), GetCameraTransform().pos, 1)
         end
 
@@ -200,3 +55,92 @@
 
 end
 
+function server.init()
+    CheckRegInitialized()
+    Init_Config()
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        ManageUiBinding()
+        if activeAssignment and InputLastPressedKey() ~= '' then
+
+            SetString(activePath, string.lower(InputLastPressedKey()), true)
+            activeAssignment = false
+            activePath = ''
+
+        end
+    end
+end
+
+function client.draw()
+    UiColor(1,1,1,1)
+    UiFont('regular.ttf', font_size)
+    UiTranslate(UiCenter(), 0)
+
+    do UiPush()
+
+        -- Title
+        do UiPush()
+            UiTranslate(0, font_size)
+            UiFont('regular.ttf', 64)
+            UiAlign('center top')
+            UiText('Flying Planes')
+
+            UiTranslate(0, 64)
+            UiFont('regular.ttf', 32)
+            UiText('By: Cheejins')
+        UiPop() end
+
+        -- Button : Start Demo Map
+        do UiPush()
+
+            UiAlign('center middle')
+            UiFont('regular.ttf', font_size*1.5)
+            UiTranslate(0, 190)
+            -- local c = Oscillate(2)/3 + 2/3
+            -- UiColor(c,c,1,1)
+            -- UiButtonImageBox("ui/common/box-outline-6.png", 10,10)
+            -- UiButtonHoverColor(0.5,0.5,1,1)
+            -- if UiTextButton('Start Demo Map', 350, font_size*2.5) then
+            --     StartLevel('', 'demo.xml', '')
+            -- end
+
+            UiTranslate(0, 80)
+            UiColor(1,1,1,1)
+
+            UiTranslate(0, font_size*2.5)
+            Ui_Option_Keybind(250, font_size*2, 0, "Change Target", Config.changeTarget, Config, "changeTarget")
+
+            UiTranslate(0, font_size*2.5)
+            Ui_Option_Keybind(250, font_size*2, 0, "Toggle Missile Homing", Config.toggleHoming, Config, "toggleHoming")
+
+            UiFont('regular.ttf', 32)
+            UiTranslate(0, font_size*3)
+            UiText("More keybinds coming soon.")
+
+        UiPop() end
+
+    UiPop() end
+
+    do UiPush()
+
+        UiTranslate(0, UiHeight() - 150)
+
+        UiAlign('center middle')
+        UiButtonImageBox('ui/common/box-outline-6.png', 10,10, 1, 1, 1, 1)
+        if UiTextButton('Reset', 150, font_size*2) then
+            ClearKey("savegame.mod")
+        end
+
+        UiTranslate(0, font_size*2.5)
+
+        UiButtonImageBox("ui/common/box-outline-6.png", 10,10)
+        UiButtonHoverColor(0.5,0.5,1,1)
+        if UiTextButton('Close', 150, font_size*2) then
+            Menu()
+        end
+
+    UiPop() end
+end
+

```

---

# Migration Report: prefab\Cessna172\Cessna172.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/prefab\Cessna172\Cessna172.lua
+++ patched/prefab\Cessna172\Cessna172.lua
@@ -1,86 +1,83 @@
-function init()
-	btn_navlight = FindShape("nl")
-	btn_cabinlight = FindShape("cl")
-	btn_instrumentlight = FindShape("ilb")
-
-	light_instrument = FindLight("instrument")
-	light_beacon = FindLight("beacon")
-	light_cabin = FindLights("cabin")
-	light_nav = FindLights("navlight")
-
-	SetTag(btn_navlight, "interact", "Navigation lights")
-	SetTag(btn_cabinlight, "interact", "Cabin lights")
-	SetTag(btn_instrumentlight, "interact", "Instrument light")
-
-	for i=1,#light_cabin do
-		SetLightEnabled(light_cabin[i], false)
-	end
-
-	for i=1,#light_nav do
-		SetLightEnabled(light_nav[i], false)
-	end
-
-	SetLightEnabled(light_instrument, false)
-	SetLightEnabled(light_beacon, false)
-
-	beacon = false
-	timer = 0
+#version 2
+function server.init()
+    btn_navlight = FindShape("nl")
+    btn_cabinlight = FindShape("cl")
+    btn_instrumentlight = FindShape("ilb")
+    light_instrument = FindLight("instrument")
+    light_beacon = FindLight("beacon")
+    light_cabin = FindLights("cabin")
+    light_nav = FindLights("navlight")
+    SetTag(btn_navlight, "interact", "Navigation lights")
+    SetTag(btn_cabinlight, "interact", "Cabin lights")
+    SetTag(btn_instrumentlight, "interact", "Instrument light")
+    for i=1,#light_cabin do
+    	SetLightEnabled(light_cabin[i], false)
+    end
+    for i=1,#light_nav do
+    	SetLightEnabled(light_nav[i], false)
+    end
+    SetLightEnabled(light_instrument, false)
+    SetLightEnabled(light_beacon, false)
+    beacon = false
+    timer = 0
 end
 
-function update(dt)
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if beacon then
+        timer = timer + 1
+        	if timer == 80 then
+        		timer = timer * 0 + 1
+        	end
+        	if timer > 0 and timer < 10 then
+        		SetLightEnabled(light_beacon, true)
+        	end
+        	if timer >= 10 and timer < 20 then
+        		SetLightEnabled(light_beacon, false)
+        	end
+        	if timer >= 20 and timer < 30 then
+        		SetLightEnabled(light_beacon, true)
+        	end
+        	if timer >= 30 and timer < 80 then
+        		SetLightEnabled(light_beacon, false)
+        	end
+        end
+    end
+end
 
-	if GetPlayerInteractShape() == btn_cabinlight and InputPressed("interact") then
-		for i=1,#light_cabin do
-			if IsLightActive(light_cabin[i]) == false then
-				SetLightEnabled(light_cabin[i], true)
-			else
-				SetLightEnabled(light_cabin[i], false)
-			end
-		end
-	end
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == btn_cabinlight and InputPressed("interact") then
+    	for i=1,#light_cabin do
+    		if IsLightActive(light_cabin[i]) == false then
+    			SetLightEnabled(light_cabin[i], true)
+    		else
+    			SetLightEnabled(light_cabin[i], false)
+    		end
+    	end
+    end
+    if GetPlayerInteractShape(playerId) == btn_navlight and InputPressed("interact") then
+    	if not beacon then
+    		beacon = true
+    	else
+    		beacon = false
+    	end
 
-	if GetPlayerInteractShape() == btn_navlight and InputPressed("interact") then
-		if not beacon then
-			beacon = true
-		else
-			beacon = false
-		end
+    	for i=1,#light_nav do
+    		if IsLightActive(light_nav[i]) == false then
+    			SetLightEnabled(light_nav[i], true)
+    		else
+    			SetLightEnabled(light_nav[i], false)
+    		end
+    	end
 
-		for i=1,#light_nav do
-			if IsLightActive(light_nav[i]) == false then
-				SetLightEnabled(light_nav[i], true)
-			else
-				SetLightEnabled(light_nav[i], false)
-			end
-		end
+    end
+    if GetPlayerInteractShape(playerId) == btn_instrumentlight and InputPressed("interact") then
+    	if IsLightActive(light_instrument) == false then
+    		SetLightEnabled(light_instrument, true)
+    	else
+    		SetLightEnabled(light_instrument, false)
+    	end
+    end
+end
 
-	end
-
-	if GetPlayerInteractShape() == btn_instrumentlight and InputPressed("interact") then
-		if IsLightActive(light_instrument) == false then
-			SetLightEnabled(light_instrument, true)
-		else
-			SetLightEnabled(light_instrument, false)
-		end
-	end
-
-	if beacon then
-	timer = timer + 1
-		if timer == 80 then
-			timer = timer * 0 + 1
-		end
-		if timer > 0 and timer < 10 then
-			SetLightEnabled(light_beacon, true)
-		end
-		if timer >= 10 and timer < 20 then
-			SetLightEnabled(light_beacon, false)
-		end
-		if timer >= 20 and timer < 30 then
-			SetLightEnabled(light_beacon, true)
-		end
-		if timer >= 30 and timer < 80 then
-			SetLightEnabled(light_beacon, false)
-		end
-	end
-
-end
```

---

# Migration Report: prefab\checkScript.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/prefab\checkScript.lua
+++ patched/prefab\checkScript.lua
@@ -1,40 +1,4 @@
-#include "../TDSU/tdsu.lua"
-
--- This script is ran for each plane that is spawned and is separate from the main script.
-
--- PLANE IDs
--- This script is responsible for processing plane parts and assigning a global ID to collection of parts.
--- In script.lua, the parts will be found using the assigned tags. The unique ID is stored in the registry.
--- It will be applied to the vehicle entity as a tag called ID and a value of an integer eg: ID=1, ID=6
-
-------------------------------------------------------------------------------------------------------------
-
-
-function init()
-
-    -- Check whether the script instance is running.
-    CheckScriptEnabled()
-
-
-    -- This int can always be used as the current ID.
-    ID = GetInt("level.Plane_ID")
-    if ID == 0 then
-        ID = 2
-    end
-    SetInt("level.Plane_ID", ID + 1)
-
-
-    -- Tag name.
-    IDTag = "Plane_ID"
-
-    -- Apply IDs
-    ApplyPlaneEntityIDs(ID)
-
-    print("checkScript")
-
-end
-
-
+#version 2
 function ApplyPlaneEntityIDs(ID)
 
     AllEntities = {
@@ -54,24 +18,38 @@
 
 end
 
-
-function tick()
-    for _, shape in ipairs(AllEntities.AllShapes) do
-        -- DrawShapeOutline(shape, 1,0,1, 0.5)
-
-        if GetShapeBody(shape) == GetWorldBody() then
-            DebugCross(AabbGetShapeCenterPos(shape), 1,0,0, 1)
-        end
-
-    end
-
-    -- DrawBodyOutline(GetWorldBody(), 1,0,0, 0.5)
-end
-
-
 function CheckScriptEnabled()
     if GetBool('level.planeScriptActive') == false then
         Spawn('MOD/prefab/script.xml', Transform())
-        SetBool('level.planeScriptActive', true)
+        SetBool('level.planeScriptActive', true, true)
     end
 end
+
+function server.init()
+    CheckScriptEnabled()
+    -- This int can always be used as the current ID.
+    ID = GetInt("level.Plane_ID")
+    if ID == 0 then
+        ID = 2
+    end
+    SetInt("level.Plane_ID", ID + 1, true)
+    -- Tag name.
+    IDTag = "Plane_ID"
+    -- Apply IDs
+    ApplyPlaneEntityIDs(ID)
+    print("checkScript")
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for _, shape in ipairs(AllEntities.AllShapes) do
+            -- DrawShapeOutline(shape, 1,0,1, 0.5)
+
+            if GetShapeBody(shape) == GetWorldBody() then
+                DebugCross(AabbGetShapeCenterPos(shape), 1,0,0, 1)
+            end
+
+        end
+    end
+end
+

```

---

# Migration Report: script\ai_planes.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\ai_planes.lua
+++ patched/script\ai_planes.lua
@@ -1,8 +1,5 @@
-AI_PLANES = {}
-AI_PLANES_NOTSET = {}
-
+#version 2
 local flightPath = {}
-
 local plane_prefabs = {
     "MOD/prefab/Mig29.xml",
     "MOD/prefab/F15.xml",
@@ -10,7 +7,6 @@
     "MOD/prefab/Harrier.xml",
 }
 
-
 function aiplanes_CreateFlightpaths()
 
     local radius = 1000
@@ -60,7 +56,6 @@
     return AutoVecSubsituteY(VecLerp(min, max), min[2])
 
 end
-
 
 function Tick_aiplanes()
 
@@ -91,8 +86,6 @@
     end
 
 end
-
-
 
 function aiplane_SpawnPlane(tr)
 
@@ -129,7 +122,6 @@
 
 end
 
--- Assigns the plane the tick after it is spawned.
 function aiplane_AssignPlanes()
 
     local planesToRemove = {}
@@ -160,8 +152,6 @@
     end
 
 end
-
-
 
 function aiplane_sound(plane)
 
@@ -199,8 +189,6 @@
 
 end
 
-
-
 function aiplane_pursue_plane(plane, targetPlane)
 
     --[[
@@ -216,7 +204,6 @@
     ]]
 
 end
-
 
 function Draw_AiplanesFlightPaths()
 
@@ -264,4 +251,5 @@
         UiPop()
     end
 
-end+end
+

```

---

# Migration Report: script\ai_SAMS.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\ai_SAMS.lua
+++ patched/script\ai_SAMS.lua
@@ -1,19 +1,7 @@
-#include "../TDSU/tdsu.lua"
-
-EnemyAAs = {}
-EnemyAAMGs = {}
-
-
-AA_Types = {
-    SAM = { title = "SAM", rpm = 20 },
-    MG = { title = "MG", rpm = 800 },
-}
-
-
+#version 2
 function Init_Enemies()
 
     Init_Utils()
-
 
     for _, v in ipairs(FindVehicles("AA", true)) do
 
@@ -39,7 +27,6 @@
 
 end
 
-
 function Manage_Enemies()
 
     Tick_Utils()
@@ -55,13 +42,12 @@
             local proj = DeepCopy(ProjectilePresets.bullets.aa)
             local shootPos = VecAdd(AabbGetBodyCenterTopPos(AA.body), Vec(0,4,0))
 
-
             -- Set target
-            AA.targetPos = GetPlayerTransform().pos
+            AA.targetPos = GetPlayerTransform(playerId).pos
 
             -- Target player
-            local playerVehicle = GetPlayerVehicle()
-            if GetPlayerVehicle() ~= 0 then
+            local playerVehicle = GetPlayerVehicle(playerId)
+            if GetPlayerVehicle(playerId) ~= 0 then
 
                 local targetVel = GetBodyVelocity(GetVehicleBody(playerVehicle))
                 local targetDist = VecDist(AA.targetPos, shootPos)/10
@@ -69,13 +55,9 @@
 
                 local bodyTr = GetBodyTransform(GetVehicleBody(playerVehicle))
 
-
                 AA.targetPos = VecAdd(bodyTr.pos, VecScale(targetVel, velScale/10))
 
-
             end
-
-
 
             -- Set up shooting.
             local shootTr = Transform(shootPos, QuatLookAt(shootPos, AA.targetPos))
@@ -88,8 +70,6 @@
                     (math.random()+0.5)
                 ))
 
-
-
             local targetShape = nil
 
             if AA.type == AA_Types.MG.title then
@@ -100,8 +80,8 @@
 
                 proj = DeepCopy(ProjectilePresets.missiles.SAM)
 
-                if IsHandleValid(GetPlayerVehicle()) then
-                local vehicle = GetPlayerVehicle()
+                if IsHandleValid(GetPlayerVehicle(playerId)) then
+                local vehicle = GetPlayerVehicle(playerId)
                 local body = GetVehicleBody(vehicle)
                 local shapes = GetBodyShapes(body)
                 local shape = shapes[math.random(1, #shapes)]
@@ -109,8 +89,6 @@
                 end
 
             end
-
-
 
             if AA.shooting then
 
@@ -135,9 +113,7 @@
                         PlayLoop(sounds.mg3, shootTr.pos, 100)
                     end
 
-
                 end
-
 
                 TimerRunTime(AA.shootTimer)
                 if TimerConsumed(AA.shootTimer) then
@@ -162,3 +138,4 @@
     end
 
 end
+

```

---

# Migration Report: script\debug.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\debug.lua
+++ patched/script\debug.lua
@@ -1,11 +1,10 @@
--- db = false
-
+#version 2
 function Manage_DebugMode()
 
     db = GetBool('savegame.mod.debugMode')
     if InputDown('ctrl') and InputDown('shift') and InputPressed('d')  then
 
-        SetBool('savegame.mod.debugMode', not GetBool('savegame.mod.debugMode'))
+        SetBool('savegame.mod.debugMode', not GetBool('savegame.mod.debugMode'), true)
         db = GetBool('savegame.mod.debugMode')
 
     end
@@ -13,7 +12,7 @@
     db_map = GetBool('savegame.mod.testMap')
     if InputDown('ctrl') and InputDown('shift') and InputPressed('c')  then
 
-        SetBool('savegame.mod.testMap', not GetBool('savegame.mod.testMap'))
+        SetBool('savegame.mod.testMap', not GetBool('savegame.mod.testMap'), true)
         db_map = GetBool('savegame.mod.testMap')
 
         if db_map then
@@ -26,21 +25,25 @@
 
 end
 
+function db_func(func) if db then func() end end
 
-function db_func(func) if db then func() end end -- debug function call
+function dbw(str, value) if db then DebugWatch(str, value) end end
 
-function dbw(str, value) if db then DebugWatch(str, value) end end -- debug watch
-function dbp(str, newLine) if db then print(str .. '(' .. sfnTime() .. ')') end end -- debug print
-function dbpc(str, newLine) if db then print(str .. Ternary(newLine, '\n', '')) end end -- debug print
+function dbp(str, newLine) if db then print(str .. '(' .. sfnTime() .. ')') end end
 
-function dbl(p1, p2, c1, c2, c3, a) if db then DebugLine(p1, p2, c1, c2, c3, a) end end -- debug line
-function dbdd(pos,w,l,r,g,b,a,dt) if db then DrawDot(pos,w,l,r,g,b,a,dt) end end -- debug draw dot
-function dbray(tr, dist, c1, c2, c3, a) dbl(tr.pos, TransformToParentPoint(tr, Vec(0,0,-dist)), c1, c2, c3, a) end -- Debug ray from transform.
-function dbcr(pos, r,g,b, a) if db then DebugCross(pos, r or 1, g or 1, b or 1, a or 1) end end -- debug cross
+function dbpc(str, newLine) if db then print(str .. Ternary(newLine, '\n', '')) end end
 
+function dbl(p1, p2, c1, c2, c3, a) if db then DebugLine(p1, p2, c1, c2, c3, a) end end
+
+function dbdd(pos,w,l,r,g,b,a,dt) if db then DrawDot(pos,w,l,r,g,b,a,dt) end end
+
+function dbray(tr, dist, c1, c2, c3, a) dbl(tr.pos, TransformToParentPoint(tr, Vec(0,0,-dist)), c1, c2, c3, a) end
+
+function dbcr(pos, r,g,b, a) if db then DebugCross(pos, r or 1, g or 1, b or 1, a or 1) end end
 
 function DebugWatchPlane(plane, title, value)
-    if plane.vehicle == GetPlayerVehicle() then
+    if plane.vehicle == GetPlayerVehicle(playerId) then
         DebugWatch(title, value)
     end
 end
+

```

---

# Migration Report: script\grenade.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\grenade.lua
+++ patched/script\grenade.lua
@@ -1,147 +1,12 @@
-
-globalConfig = {
-        gravity = Vec(0,-9,0)
- }
-
-weapon = {
-	 weaponName 				= "grenade",
-  	munitionType 			= "explosive",
-  	explosionSize 		= 1,
-  	fuze_time 				= 5,
-    fuze_sensitivity = 0.25,
-    reliability       = .25, -- (percentage deviation from expected explosion time)
-    shrapnel_damage =  3,
-    shrapnel_size     =0.2,
-    spall_value = 200,
-    jet_vel = 150,
-    cone = 15,
-
-  	Create 					= "elboydo",
-}
-
-spallHandler =
-  {
-    shellNum = 1,
-    shells = {
-
-    },
-  defaultShell = {active=false, velocity=nil, direction =nil, currentPos=nil, timeLaunched=nil},
-  velocity = 200,
-  gravity = Vec(0,-25,0),
-  shellWidth = 0.3,
-  shellHeight = 0.3,
-  }
-
-
-boom_pos = nil
-
-
-warhead_primed = false
-
-active_spall = 0
-
-total_spall = 0
-
-
-function init( )
-  munition  = FindShape(weapon.weaponName)
-  body = GetShapeBody(munition)
-  -- DebugWatch("body vel at init",VecLength(GetBodyVelocity(body)))
-
-  last_vel_dir =  GetBodyVelocity(body)
-  last_vel = VecLength(GetBodyVelocity(body))
-  fuze = weapon.fuze_time + rnd(-weapon.fuze_time * weapon.reliability,weapon.fuze_time * weapon.reliability)
-  added_cook_time = false
-
-  exploded = false
-  explosion_sound = LoadSound("MOD/snd/grenade_explosion.ogg")
-  spalling_sprite =  LoadSprite("MOD/gfx/spalling.png")
-  vehicle = GetPlayerVehicle()
-  vehiclebody = GetVehicleBody(vehicle)
-  local munition_body = GetShapeBody(munition)
-  vehiclebodyvelocity = GetBodyVelocity(vehiclebody)
-  SetBodyVelocity(munition_body, vehiclebodyvelocity)
-
-end
+#version 2
 function rnd(mi, ma)
   return math.random()*(ma-mi)+mi
 end
+
 function rndVec(length)
   local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
   return VecScale(v, length)
 end
-function tick(dt)
-  -- if(boom_pos~=nil) then
-  --   DebugCross(boom_pos)
-  -- end
-  -- DebugWatch("active spall ",active_spall)
-  -- DebugWatch("total spall ",total_spall)
-
-  -- DebugWatch("body vel in flight",VecLength(GetBodyVelocity(body)))
-
-  if(not exploded) then
-
-
-        local calibreCoef = 1
-        local exaust_pos = TransformToParentPoint(GetShapeWorldTransform(munition),Vec(0,0.8,-0.3))
-        local exaust_vec = VecSub(GetShapeWorldTransform(munition).pos, TransformToParentPoint(GetShapeWorldTransform(munition),Vec(0,1,-10)))
-        SpawnParticle("fire",exaust_pos, exaust_vec,  1.1*calibreCoef, .15)
-        SpawnParticle("smoke",exaust_pos, exaust_vec, 1.2*calibreCoef, .3)
-        PointLight(exaust_pos, 0.8, 0.8, 0.5, math.random(1*calibreCoef,15*calibreCoef))
-        local munition_body = GetShapeBody(munition)
-        local speed_limit = 280
-        if(VecLength(GetBodyVelocity(munition_body))<speed_limit) then
-
-          local nose_pos = GetBodyCenterOfMass(GetShapeBody(munition))--TransformToParentPoint(GetShapeWorldTransform(munition),Vec(0,0.8,0.3))
-          local munition_centre = Transform(nose_pos,QuatCopy(GetShapeWorldTransform(munition).rot))
-          local thrust_vec = VecSub(munition_centre.pos,TransformToParentPoint(munition_centre,Vec(0,-160, -9)))--VecSub(GetShapeWorldTransform(munition).pos, TransformToParentPoint(GetShapeWorldTransform(munition),Vec(00,-10, 0)))
-          SetBodyVelocity(munition_body,VecAdd(GetBodyVelocity(munition_body),VecScale(thrust_vec,dt)))
-        else
-          local body_vel = GetBodyVelocity(munition_body)
-          SetBodyVelocity(munition_body,VecScale(body_vel,speed_limit/VecLength(body_vel)))
-        end
-        -- DebugWatch("MUNITION VEL",VecLength(GetBodyVelocity(munition_body)))
-        --ApplyBodyImpulse(GetShapeBody(munition),nose_pos,VecScale(thrust_vec,80*dt))
-        -- local pos = GetShapeWorldTransform(munition)
-        -- local calibreCoef = 10
-        -- ParticleReset()
-        -- ParticleType("smoke")
-        -- ParticleColor(0.7, 0.6, 0.5)
-        -- --Spawn particle at world origo with upwards velocity and a lifetime of ten seconds
-        -- SpawnParticle(Vec(0, 0, 0), Vec(0, 1, 0), 10.0)
-        -- PointLight(pos, 0.8, 0.8, 0.5, math.random(1*calibreCoef,15*calibreCoef))
-
-
-    if(warhead_primed) then
-      if(fuze>0) then
-        fuze = fuze - dt
-        if(fuze_triggered(GetBodyVelocity(body))) then
-          fuze = -1
-        end
-      else
-        local pos = GetShapeWorldTransform(munition).pos
-        local explode_pos = TransformToParentPoint(GetShapeWorldTransform(munition),Vec(0,0,0.5))
-        Explosion(explode_pos,weapon.explosionSize)
-        PlaySound(explosion_sound, pos,50)
-        local shrapnel_pos = TransformToParentPoint(GetShapeWorldTransform(munition),Vec(0,1.6,0))
-        boom_pos = shrapnel_pos
-        pushshrapnel(Transform(shrapnel_pos))
-        exploded = true
-      end
-    else
-
-         if VecLength(GetBodyVelocity(body))> 10 and  fuze_triggered(GetBodyVelocity(body)) then
-          warhead_primed = true
-          last_vel_dir = GetBodyVelocity(body)
-          last_vel = VecLength(GetBodyVelocity(body))
-        end
-    end
-  elseif(active_spall>0) then
-    spallingTick(dt)
-  end
-
-end
-
 
 function fuze_triggered(t_vel)
   vel = VecLength(t_vel)
@@ -156,7 +21,6 @@
         return false
     end
 end
-
 
 function pushshrapnel(spallingLoc)
 
@@ -201,13 +65,11 @@
     currentSpall.shellType.g = 1.7 + (math.random(0,5)/10)
     currentSpall.shellType.b = 1 + (math.random(0,10)/10)
 
-
     spallHandler.shellNum = (spallHandler.shellNum%#spallHandler.shells) +1
 
   end
 
 end
-
 
 function shrapnelOperations(projectile,dt )
     projectile.cannonLoc.pos = projectile.point1
@@ -219,7 +81,6 @@
     local g = projectile.shellType.g * spallDecay
     local b = projectile.shellType.b * spallDecay
 
-
     --- sprite drawing
     DrawSprite(spalling_sprite, projectile.cannonLoc,projectile.shellType.shellWidth,shellHeight , r, g, b, 1, 0, false)
     local altloc = TransformCopy(projectile.cannonLoc)
@@ -228,7 +89,6 @@
     altloc.rot = QuatRotateQuat(projectile.cannonLoc.rot,QuatEuler(90, 0,0))
     DrawSprite(spalling_sprite, altloc, projectile.shellType.shellWidth, projectile.shellType.shellWidth, r, g, b, 1, 0, false)
 
-
     projectile.predictedBulletVelocity = VecScale(projectile.predictedBulletVelocity,0.8)
 
     local dispersion = Vec(math.random(-1,1)*projectile.dispersion,math.random(-1,1)*projectile.dispersion,math.random(-1,1)*projectile.dispersion)
@@ -244,8 +104,6 @@
     local hit, dist1,norm1,shape1 = QueryRaycast(projectile.point1, VecNormalize(VecSub(point2,projectile.point1)),VecLength(VecSub(point2,projectile.point1)))
 
     projectile.cannonLoc.rot = QuatRotateQuat(QuatLookAt(point2,projectile.point1),QuatEuler(00, 90, 90))
-
-
 
       local hit_player =  inflict_player_damage(projectile,point2)
 
@@ -260,10 +118,7 @@
 
 end
 
-
-
 function popSpalling(shell,hitTarget)
-
 
     local holeModifier = math.random(-15,15)/100
     local fireChance = math.random(0,100)/100
@@ -293,7 +148,6 @@
     shell = DeepCopy(spallHandler.defaultShell)
 
 end
-
 
 function spallingTick(dt)
       -- DebugWatch("shells",#spallHandler.shells  )
@@ -315,8 +169,6 @@
     end
 end
 
-
-
 function inflict_player_damage(projectile,point2)
   local t= Transform(projectile.point1,QuatLookAt(point2,projectile.point1))
   local p = TransformToParentPoint(t, Vec(0, 0, 1))
@@ -326,15 +178,15 @@
 
   hurt_dist = VecLength(VecSub(projectile.point1,point2))
   --Hurt player
-  local player_cam_pos = GetPlayerCameraTransform().pos
-  local player_pos = GetPlayerTransform().pos
+  local player_cam_pos = GetPlayerCameraTransform(playerId).pos
+  local player_pos = GetPlayerTransform(playerId).pos
 
   player_pos = VecLerp(player_pos,player_cam_pos,0.5)
   local toPlayer = VecSub(player_pos, t.pos)
   local distToPlayer = VecLength(toPlayer)
   local distScale = clamp(1.0 - distToPlayer / hurt_dist, 0.0, 1.0)
   -- DebugWatch("test",distScale)
-  if distScale > 0 then
+  if distScale ~= 0 then
     -- DebugWatch("dist scale",distScale)
     toPlayer = VecNormalize(toPlayer)
     -- DebugWatch("dot to player",VecDot(d, toPlayer))
@@ -345,22 +197,18 @@
       local hit = QueryRaycast(p, toPlayer, distToPlayer)
       if not hit or distToPlayer < 0.7 then
         -- DebugWatch("player would be hit",distToPlayer)
-        SetPlayerHealth(GetPlayerHealth() - 0.035 * (projectile.shellType.bulletdamage[1] * (distScale*2)*25)*math.log(VecLength(projectile.predictedBulletVelocity)))
+        SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.035 * (projectile.shellType.bulletdamage[1] * (distScale*2)*25)*math.log(VecLength(projectile.predictedBulletVelocity)))
         return true
       end
     end
   end
   return false
 end
-
-
-
 
 function clamp(val, lower, upper)
     if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
     return math.max(lower, math.min(upper, val))
 end
-
 
 function DeepCopy(orig)
     local orig_type = type(orig)
@@ -376,3 +224,87 @@
     end
     return copy
 end
+
+function server.init()
+    munition  = FindShape(weapon.weaponName)
+    body = GetShapeBody(munition)
+    -- DebugWatch("body vel at init",VecLength(GetBodyVelocity(body)))
+    last_vel_dir =  GetBodyVelocity(body)
+    last_vel = VecLength(GetBodyVelocity(body))
+    fuze = weapon.fuze_time + rnd(-weapon.fuze_time * weapon.reliability,weapon.fuze_time * weapon.reliability)
+    added_cook_time = false
+    exploded = false
+    spalling_sprite =  LoadSprite("MOD/gfx/spalling.png")
+    vehicle = GetPlayerVehicle(playerId)
+    vehiclebody = GetVehicleBody(vehicle)
+    local munition_body = GetShapeBody(munition)
+    vehiclebodyvelocity = GetBodyVelocity(vehiclebody)
+    SetBodyVelocity(munition_body, vehiclebodyvelocity)
+end
+
+function client.init()
+    explosion_sound = LoadSound("MOD/snd/grenade_explosion.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if(not exploded) then
+
+          local calibreCoef = 1
+          local exaust_pos = TransformToParentPoint(GetShapeWorldTransform(munition),Vec(0,0.8,-0.3))
+          local exaust_vec = VecSub(GetShapeWorldTransform(munition).pos, TransformToParentPoint(GetShapeWorldTransform(munition),Vec(0,1,-10)))
+          SpawnParticle("fire",exaust_pos, exaust_vec,  1.1*calibreCoef, .15)
+          SpawnParticle("smoke",exaust_pos, exaust_vec, 1.2*calibreCoef, .3)
+          PointLight(exaust_pos, 0.8, 0.8, 0.5, math.random(1*calibreCoef,15*calibreCoef))
+          local munition_body = GetShapeBody(munition)
+          local speed_limit = 280
+          if(VecLength(GetBodyVelocity(munition_body))<speed_limit) then
+
+            local nose_pos = GetBodyCenterOfMass(GetShapeBody(munition))--TransformToParentPoint(GetShapeWorldTransform(munition),Vec(0,0.8,0.3))
+            local munition_centre = Transform(nose_pos,QuatCopy(GetShapeWorldTransform(munition).rot))
+            local thrust_vec = VecSub(munition_centre.pos,TransformToParentPoint(munition_centre,Vec(0,-160, -9)))--VecSub(GetShapeWorldTransform(munition).pos, TransformToParentPoint(GetShapeWorldTransform(munition),Vec(00,-10, 0)))
+            SetBodyVelocity(munition_body,VecAdd(GetBodyVelocity(munition_body),VecScale(thrust_vec,dt)))
+          else
+            local body_vel = GetBodyVelocity(munition_body)
+            SetBodyVelocity(munition_body,VecScale(body_vel,speed_limit/VecLength(body_vel)))
+          end
+          -- DebugWatch("MUNITION VEL",VecLength(GetBodyVelocity(munition_body)))
+          --ApplyBodyImpulse(GetShapeBody(munition),nose_pos,VecScale(thrust_vec,80*dt))
+          -- local pos = GetShapeWorldTransform(munition)
+          -- local calibreCoef = 10
+          -- ParticleReset()
+          -- ParticleType("smoke")
+          -- ParticleColor(0.7, 0.6, 0.5)
+          -- --Spawn particle at world origo with upwards velocity and a lifetime of ten seconds
+          -- SpawnParticle(Vec(0, 0, 0), Vec(0, 1, 0), 10.0)
+          -- PointLight(pos, 0.8, 0.8, 0.5, math.random(1*calibreCoef,15*calibreCoef))
+
+      if(warhead_primed) then
+        if(fuze>0) then
+          fuze = fuze - dt
+          if(fuze_triggered(GetBodyVelocity(body))) then
+            fuze = -1
+          end
+        else
+          local pos = GetShapeWorldTransform(munition).pos
+          local explode_pos = TransformToParentPoint(GetShapeWorldTransform(munition),Vec(0,0,0.5))
+          Explosion(explode_pos,weapon.explosionSize)
+          PlaySound(explosion_sound, pos,50)
+          local shrapnel_pos = TransformToParentPoint(GetShapeWorldTransform(munition),Vec(0,1.6,0))
+          boom_pos = shrapnel_pos
+          pushshrapnel(Transform(shrapnel_pos))
+          exploded = true
+        end
+      else
+
+           if VecLength(GetBodyVelocity(body))> 10 and  fuze_triggered(GetBodyVelocity(body)) then
+            warhead_primed = true
+            last_vel_dir = GetBodyVelocity(body)
+            last_vel = VecLength(GetBodyVelocity(body))
+          end
+      end
+    elseif(active_spall>0) then
+      spallingTick(dt)
+    end
+end
+

```

---

# Migration Report: script\input\controlPanel.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\input\controlPanel.lua
+++ patched/script\input\controlPanel.lua
@@ -1,6 +1,4 @@
-UiControls = {}
-
-
+#version 2
 function getImgPath(str)
     return 'MOD/img/icon_' .. str .. '.png'
 end
@@ -41,7 +39,6 @@
         ''
     )
 
-
     createUiControl(
         'prevCamera',
         'camera_prev',
@@ -55,7 +52,6 @@
         ''
     )
 
-
     createUiControl(
         'prevEvent',
         'event_prev',
@@ -68,7 +64,6 @@
         'NextEvent',
         ''
     )
-
 
     createUiControl(
         'detailedMode',
@@ -89,7 +84,6 @@
         ''
     )
 
-
     createUiControl(
         'toggleUi',
         'toggleUi',
@@ -105,35 +99,40 @@
 
 end
 
-
 function toggleDrawCameras()
     DRAW_CAMERAS = not DRAW_CAMERAS
 end
+
 function togglePinControlPanel()
     UI_PIN_CONTROL_PANEL = not UI_PIN_CONTROL_PANEL
 end
+
 function toggleDetails()
     UI_SHOW_DETAILS = not UI_SHOW_DETAILS
 end
+
 function toggleShowUi()
     UI_SHOW_OPTIONS = not UI_SHOW_OPTIONS
 end
+
 function toggleViewCamera()
     RUN_CAMERAS = not RUN_CAMERAS
     validateItemChain()
 end
+
 function clearAllObjects()
     ITEM_OBJECTS = {}
     ITEM_CHAIN = {}
     EVENT_OBJECTS = {}
     CAMERA_OBJECTS = {}
 end
+
 function toggleRunChain()
     RUN_ITEM_CHAIN = not RUN_ITEM_CHAIN
     validateItemChain()
 end
 
-
 function shouldDisableControlPanel()
     return activeAssignment or activeNameAssignment
-end+end
+

```

---

# Migration Report: script\input\input.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\input\input.lua
+++ patched/script\input\input.lua
@@ -1,29 +1,4 @@
-keyTitles = {
-    leftarrow   = 'left',
-    rightarrow  = 'right',
-    uparrow     = 'up',
-    downarrow   = 'down',
-}
-
-validKeys = {
-    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
-    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
-    'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
-    'tab', 'uparrow', 'downarrow', 'leftarrow', 'rightarrow',
-    'backspace', 'alt', 'delete', 'home', 'end',
-    'pgup', 'pgdown', 'insert', 'space', 'shift', 'ctrl', 'return', 'rmb', 'mmb',
-}
-
-validChars = {
-    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
-    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
-    'space',
-}
-
-comboKeys = {'-', 'ctrl', 'shift', 'alt'}
-
-
---- Convert a input string to the appropriate display string.
+#version 2
 function convertKeyTitle(str)
     for key, value in pairs(keyTitles) do
         if key == str then
@@ -33,7 +8,6 @@
     return str
 end
 
---- Check if a string is a valid keyboard input.
 function isKeyValid(str)
     for index, value in ipairs(validKeys) do
         if str == value then
@@ -43,7 +17,6 @@
     return false
 end
 
---- Check if a string is a valid text input.
 function isCharValid(str)
     for index, value in ipairs(validChars) do
         if str == value then
@@ -53,9 +26,6 @@
     return false
 end
 
-
-
--- Manages user input.
 function ManageInput()
 
     -- if InputDown(KEYS.pinPanel.key1) and InputPressed(KEYS.pinPanel.key2) then
@@ -69,7 +39,6 @@
             local control = UiControls[i]
 
             local noComboKey = KEYS[control.name].key1 == '-'
-
 
             if noComboKey then
 
@@ -94,3 +63,4 @@
     -- end
 
 end
+

```

---

# Migration Report: script\input\keybinds.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\input\keybinds.lua
+++ patched/script\input\keybinds.lua
@@ -1,123 +1,4 @@
-Actions = {
-    shoot_primary,
-    shoot_secondary,
-    homing,
-    thrust_increase,
-    thrust_decrease,
-    pitch_up,
-    pitch_down,
-    roll_left,
-    roll_right,
-    yaw_left,
-    yaw_right,
-    airbrake,
-    freecam,
-    change_camera,
-    next_target,
-    disable_input,
-}
-
-
-Keys = {
-
-    Weapons = {
-        {
-            key =     "lmb",
-            action =  "shoot_primary",
-            title =   "Shoot primary",
-        },
-        {
-            key =     "rmb",
-            action =  "shoot_secondary",
-            title =   "Shoot secondary",
-        },
-        {
-            key =     "h",
-            action =  "homing",
-            title =   "Toggle missile homing on/off",
-        },
-    },
-
-    Movement = {
-        {
-            key =     "shift",
-            action =  "thrust_increase",
-            title =   "Thrust increase",
-        },
-        {
-            key =     "ctrl",
-            action =  "thrust_decrease",
-            title =   "Thrust decrease",
-        },
-        {
-            key =     "s",
-            action =  "pitch_up",
-            title =   "Pitch up",
-        },
-        {
-            key =     "w",
-            action =  "pitch_down",
-            title =   "Pitch down",
-        },
-        {
-            key =     "a",
-            action =  "roll_left",
-            title =   "Roll left",
-        },
-        {
-            key =     "d",
-            action =  "roll_right",
-            title =   "Roll right",
-        },
-        {
-            key =     "z",
-            action =  "yaw_left",
-            title =   "Yaw left",
-        },
-        {
-            key =     "c",
-            action =  "yaw_right",
-            title =   "Yaw right",
-        },
-        {
-            key =     "space",
-            action =  "airbrake",
-            title =   "Airbrake",
-        },
-    },
-
-    Camera = {
-        {
-            key =     "x",
-            action =  "freecam",
-            title =   "Free camera (hold)",
-        },
-        {
-            key =     "r",
-            action =  "change_camera",
-            title =   "Switch to the next camera view",
-        },
-    },
-
-    Targeting = {
-        {
-            key =     "q",
-            action =  "next_target",
-            title =   "Select next target",
-        },
-    },
-
-    Misc = {
-        {
-            key =     "k",
-            action =  "disable_input",
-            title =   "Temporarily disable all plane inputs.",
-        },
-    },
-
-}
-
-
+#version 2
 function InitKeys()
 
     KEYS = util.shared_table("savegame.mod.keys", Keys)
@@ -133,7 +14,6 @@
 
 end
 
-
 function ConvertSharedTable(_path)
 
     local tb = {}
@@ -147,12 +27,12 @@
     return tb
 
 end
+
 function BuildSharedTableValue(tb, key, _path)
 
     local pathConc = conc(_path, {key})
     local pathConcType = conc(pathConc, {'type'})
     local pathConcVal = conc(pathConc, {'val'})
-
 
     -- Get value type.
     local type = GetString(pathConcType)
@@ -162,7 +42,6 @@
     elseif type == 'number'  then tb[key] = GetFloat(pathConcVal)
     elseif type == 'string'  then tb[key] = GetString(pathConcVal)
     end
-
 
     -- Build nested table.
     if type == 'table' then
@@ -201,9 +80,6 @@
 
 end
 
-
-
---- Concat reg path and key.
 function conc(path, k)
 
     if type(k) == 'table' then
@@ -225,6 +101,8 @@
     end
     return result
 end
+
 function trim(s)
     return (s:gsub("^%s*(.-)%s*$", "%1"))
-end+end
+

```

---

# Migration Report: script\keybinds.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\keybinds.lua
+++ patched/script\keybinds.lua
@@ -1,132 +1 @@
--- function InitKeys()
-
---     KEYS = util.structured_table("savegame.mod.keys", {
-
---         -- Weapons
---         shoot_primary = {
---             title = { 'string', 'Shoot primary' },
---             keys = {
---                 key = 'string', 'lmb',
---                 modifier = { 'string', ' ' }
---             },
---         },
---         shoot_secondary = {
---             title = { 'string', 'Shoot secondary' },
---             keys = {
---                 key = 'string', 'rmb',
---                 modifier = { 'string', ' ' },
---             },
---         },
-
-
---         -- Movement controls.
---         thrust_add = {
---             title = { 'string', 'Thrust increase' },
---             keys = {
---                 key = 'string', 'w',
---                 modifier = { 'string', ' ' },
---             },
---         },
---         thrust_sub = {
---             title = { 'string', 'Thrust decrease' },
---             keys = {
---                 key = 'string', 's',
---                 modifier = { 'string', ' ' },
---             },
---         },
---         roll_left = {
---             title = { 'string', 'Roll left' },
---             keys = {
---                 key = 'string', 'up',
---                 modifier = { 'string', ' ' },
---             },
---         },
---         roll_right = {
---             title = { 'string', 'Roll right' },
---             keys = {
---                 key = 'string', 'left',
---                 modifier = { 'string', ' ' },
---             },
---         },
---         yaw_left = {
---             title = { 'string', 'Yaw left' },
---             keys = {
---                 key = 'string', 'a',
---                 modifier = { 'string', ' ' },
---             },
---         },
---         yaw_right = {
---             title = { 'string', 'Yaw right' },
---             keys = {
---                 key = 'string', 'd',
---                 modifier = { 'string', ' ' },
---             },
---         },
---         airbrake = {
---             title = { 'string', 'Airbrake' },
---             keys = {
---                 key = 'string', 'space',
---                 modifier = { 'string', ' ' },
---             },
---         },
-
-
---         -- Camera
---         freecam = {
---             title = { 'string', 'Free camera (hold)' },
---             keys = {
---                 key = 'string', 'lmb',
---                 modifier = { 'string', ' ' },
---             },
---         },
---         resetCameraAlignment = {
---             title = { 'string', 'Reset camera alignment' },
---             keys = {
---                 key = 'string', 'lmb',
---                 modifier = { 'string', ' ' },
---             },
---         },
-
-
---         -- Targeting
---         changeTarget = {
---             title = { 'string', 'Reset camera alignment' },
---             keys = {
---                 key = 'string', 'lmb',
---                 modifier = { 'string', ' ' },
---             },
---         },
---         toggleHoming = {
---             title = { 'string', 'Toggle missile homing on/off' },
---             keys = {
---                 key = 'string', 'lmb',
---                 modifier = { 'string', ' ' },
---             },
---         },
-
---     })
-
---     print(KEYS.shoot_primary.key)
---     print('Done KEYS')
-
--- end
-
--- UiControls = {}
-
-
--- function createUiControl(name, func, gb_key)
-
---     local co = {
---         name = name,
---         keybind = { key1 = KEYS[name].key1, key2 = KEYS[name].key2 },
---         title = KEYS[name].title,
---     }
-
---     table.insert(UiControls, co)
-
--- end
-
-
--- function CreateKeyBind()
-
--- end+#version 2

```

---

# Migration Report: script\particles.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\particles.lua
+++ patched/script\particles.lua
@@ -1,3 +1,4 @@
+#version 2
 function exhaust_particle_afterburner(tr, amt, vel, alpha, emmissive)
 
     -- Flame particles.
@@ -19,8 +20,7 @@
 
  end
 
-
- function particle_fire(pos, rad)
+function particle_fire(pos, rad)
 
     ParticleReset()
 
@@ -113,3 +113,4 @@
     SpawnParticle(pos, vel, 5)
 
 end
+

```

---

# Migration Report: script\plane\plane_animate.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\plane\plane_animate.lua
+++ patched/script\plane\plane_animate.lua
@@ -1,6 +1,4 @@
----comment
----@param plane table
----@param controlsVec table Vec which contains data for pitch, yaw and roll.
+#version 2
 function plane_Animate_AeroParts(plane, ignore_input)
 
     local sub_dir = Vec(0,0,0)
@@ -11,7 +9,7 @@
             local plane_dir = Vec(GetQuatEuler(plane.tr.rot))
             sub_dir = VecSub(plane_dir, cam_dir)
 
-            -- if plane.vehicle == GetPlayerVehicle() then
+            -- if plane.vehicle == GetPlayerVehicle(playerId) then
             --     DebugWatch("sub_dir", sub_dir)
             -- end
 
@@ -28,7 +26,6 @@
     local c = InputDown("c") or (sub_dir[2] > dead_zone)
     local z = InputDown("z") or (sub_dir[2] < -dead_zone)
 
-
     -- Aero part animations.
     for parts_key, parts in pairs(plane.parts.aero) do
         for part_key, part in ipairs(parts) do
@@ -56,10 +53,8 @@
                     DebugCross(parentTr.pos, 0,1,0, 1)
                 end
 
-
                 ConstrainPosition(part.body, plane.body, pivot_tr.pos, parentTr.pos)
                 plane_Animate_AeroParts_Paralell(plane, part, pivot_tr.rot, parentTr.rot, aero_rate)
-
 
                 if not ignore_input then
 
@@ -75,7 +70,6 @@
 
                     end
 
-
                     if parts_key == "elevator" then
 
                         if w or s or a or d then
@@ -98,7 +92,6 @@
 
                     end
 
-
                     if parts_key == "aileron" then
 
                         if w or s or a or d then
@@ -121,7 +114,6 @@
 
                     end
 
-
                     if parts_key == "flap" then
 
                         if plane.flaps then
@@ -138,7 +130,6 @@
 
         end
     end
-
 
     -- Check whether to initiate landing gear transition.
     if plane.landing_gear.startTransition then
@@ -147,14 +138,12 @@
     end
     TimerRunTime(plane.landing_gear.retract_timer)
 
-
     if plane.vtol.startTransition then
         plane.vtol.startTransition = false
         TimerResetTime(plane.vtol.retract_timer)
     end
     TimerRunTime(plane.vtol.retract_timer)
 
-
     -- Landing gear constraints.
     for index, gear in ipairs(plane.parts.landing_gear) do
 
@@ -164,7 +153,6 @@
 
             local parentTr = TransformToParentTransform(plane.tr, gear.localTr) -- Tr on plane body.
             local pivot_tr = GetLightTransform(gear.light)
-
 
             local gear_alive = GetShapeVoxelCount(gear.shape)/gear.voxels > 0.5
             if gear_alive then
@@ -182,11 +170,9 @@
                 plane_Animate_AeroParts_Paralell(plane, gear, gearRot, parentTr.rot, math.huge)
                 ConstrainPosition(gear.body, plane.body, pivot_tr.pos, parentTr.pos)
 
-
                 if not TimerConsumed(plane.landing_gear.retract_timer) then
                     PlayLoop(loops.landing_gear, pivot_tr.pos, 1.5)
                 end
-
 
                 -- local vTr = GetVehicleTransform(gear.vehicle) -- Top of gear (pivot point)
                 -- local bTr = GetBodyTransform(gear.body) -- Bottom of gear (wheel)
@@ -199,7 +185,6 @@
                 --     local rv = dist - rcdist
                 --     local rv_totalVel = (dist - rcdist)/(plane.totalVel+1)
                 --     local rv_inverse = 1/rcdist/dist
-
 
                 --     if index == 1 then
                 --         DebugWatch("rv ", rv)
@@ -207,30 +192,24 @@
                 --         DebugWatch("rv_totalVel ", rv_totalVel)
                 --     end
 
-
                 --     local gear_pos_offset = VecAdd(pivot_tr.pos,Vec(0,-rv,0))
                 --     DebugCross(gear_pos_offset, 1,0,0, 1)
 
-
                 --     -- Hold pivot point of landing gear to plane body
                 --     ConstrainPosition(gear.body, plane.body, VecAdd(pivot_tr.pos, Vec(0,-rv,0)), parentTr.pos)
 
-
                 --     -- ConstrainVelocity(plane.body, GetWorldBody(), gear_pos_offset, Vec(0,1,0), rv_totalVel, 0)
-
 
                 --     if Config.debug then
                 --         DrawDot(rcpos, 1/3,1/3, 1,1,1, 1)
                 --         DebugLine(tr.pos, rcpos, 1,1,1, 1)
                 --     end
 
-
                 -- else -- Wheels are not touching anything.
 
                 --     ConstrainPosition(gear.body, plane.body, pivot_tr.pos, parentTr.pos)
 
                 -- end
-
 
                 if Config.debug then
                     DrawShapeOutline(gear.shape, 0,1,0, 1)
@@ -250,7 +229,6 @@
 
     end
 
-
     -- VTOL constraints.
     for index, vtol in ipairs(plane.parts.vtol) do
 
@@ -258,7 +236,6 @@
 
             local parentTr = TransformToParentTransform(plane.tr, vtol.localTr) -- Tr on plane body.
             local pivot_tr = GetLightTransform(vtol.light)
-
 
             -- local vtol_alive = GetShapeVoxelCount(vtol.shape)/vtol.voxels > 0.5
             -- if vtol_alive then
@@ -276,7 +253,6 @@
                 plane_Animate_AeroParts_Paralell(plane, vtol, gearRot, parentTr.rot, math.huge)
                 ConstrainPosition(vtol.body, plane.body, pivot_tr.pos, parentTr.pos)
 
-
                 if not TimerConsumed(plane.vtol.retract_timer) then
                     PlayLoop(loops.landing_gear, pivot_tr.pos, 1.5)
                 end
@@ -295,13 +271,12 @@
 
 end
 
-
 function plane_Animate_AeroParts_Paralell(part, plane, part_rot, target_rot, rate)
     ConstrainOrientation(part.body, plane.body, target_rot, part_rot, rate)
 end
 
-
 function GetPartSideSign(part)
     if part.side == "right" then return 1 end
     return -1
-end+end
+

```

---

# Migration Report: script\plane\plane_builder.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\plane\plane_builder.lua
+++ patched/script\plane\plane_builder.lua
@@ -1,47 +1,4 @@
--- AERO PARTS
-
-    -- Part types
-        -- center parts are universal, such as flaps and rudders which always align with the plane.
-        -- Parts like ailerons should be left or right since they rotate in the opposite direction of one another.
-        -- Parts like 2 parallel rudders (mig29, f15m, etc) should be tagged "rudder=center" since they rotate in the same direction.
-        -- Aero parts will use the rotations they are spawned with as their default return position.
-
-    -- Lights and Joints
-        -- Make sure to use hinge joints with no limits. The limits and angling will be controlled by the script using constrain functions.
-        -- Each joint should have a light entity placed at the same position as it in the shape. Since the API doesn't allow you to get the transform of joints,
-        -- the lights will supplement their transforms so the script knows where to angle the part from.
-
--- LANDING GEAR
-
-    -- Each landing gear compound is a vehicle (required to use a wheel). It's parts are:
-        -- body = holds the wheel entity and the single landing gear shape.
-        -- shape = within the body and holds the light entity, similar to the aero parts. Only one shape is allowed and must contain the pivot light.
-        -- light = has the tag "pivot" with a value that represents the total degrees the landing gear contracts/expands. Example: pivot=90.
-
-
-
-PlaneParts = {
-
-    aero = {
-        rudder = {},
-        elevator = {},
-        aileron = {},
-        flap = {},
-    },
-
-    landing_gear = {},
-
-    vtol = {},
-
-    systems = {
-        engines = {}
-    }
-
-}
-
-
----Builds a part object.
----@param shape number A part is a single shape.
+#version 2
 function plane_BuildPart_Aero(plane, shape, side)
 
     local light_pivot = GetShapeLights(shape)
@@ -72,11 +29,9 @@
 
 end
 
-
 function plane_CollectParts_Aero(plane)
 
     local planeParts = DeepCopy(PlaneParts)
-
 
     local AllVehicles  = FindVehicles("Plane_ID", true)
     local AllBodies    = FindBodies("Plane_ID", true)
@@ -85,7 +40,6 @@
     local AllLocations = FindLocations("Plane_ID", true)
     local AllTriggers  = FindTriggers("Plane_ID", true)
 
-
     plane.AllVehicles  = ExtractAllEntitiesByTagValue(AllVehicles,   "Plane_ID", plane.id)
     plane.AllBodies    = ExtractAllEntitiesByTagValue(AllBodies,     "Plane_ID", plane.id)
     plane.AllShapes    = ExtractAllEntitiesByTagValue(AllShapes,     "Plane_ID", plane.id)
@@ -93,13 +47,11 @@
     plane.AllLocations = ExtractAllEntitiesByTagValue(AllLocations,  "Plane_ID", plane.id)
     plane.AllTriggers  = ExtractAllEntitiesByTagValue(AllTriggers,   "Plane_ID", plane.id)
 
-
     if Config.unbreakable_planes then
         for index, shape in ipairs(plane.AllShapes) do
             SetTag(shape, "unbreakable")
         end
     end
-
 
     -- Aero parts
     for _, shape in ipairs(AllShapes) do
@@ -122,7 +74,6 @@
         end
 
     end
-
 
     -- Landing gear
     for index, vehicle in ipairs(AllVehicles) do
@@ -159,7 +110,6 @@
         end
     end
 
-
     -- VTOL thrusters
     for index, shape in ipairs(AllShapes) do
 
@@ -189,7 +139,6 @@
         end
     end
 
-
     -- Find shapes to delete.
     local deleteShapes = {}
     for index, shape in ipairs(plane.AllShapes) do
@@ -213,10 +162,6 @@
 
 end
 
-
-
-
--- Find entities of a specific type (shape, body etc...) with the relevant id tag.
 function ExtractAllEntitiesByTagValue(entity_table, tag, tag_value)
 
     local entities = {}
@@ -248,4 +193,5 @@
         end
     end
     print("Entity: " .. tag .. " not found.")
-end+end
+

```

---

# Migration Report: script\plane\plane_camera.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\plane\plane_camera.lua
+++ patched/script\plane\plane_camera.lua
@@ -1,19 +1,10 @@
-local timer_auto_center = { time = 0, rpm = 60/3 } -- Time before beginning auto centering.
-
-
-CameraPositions = {
-    "Orbit",
-    "Aligned",
-    -- "Vehicle",
-    "Seat"
-}
-
+#version 2
+local timer_auto_center = { time = 0, rpm = 60/3 }
 
 function plane_ManageCamera(plane, auto_center_delay)
 
     -- Get mouse input.
 	local mx, my = InputValue("mousedx"), InputValue("mousedy")
-
 
     -- Reset auto center delay if mouse input.
     if auto_center_delay ~= nil and (math.abs(mx) > 10 or math.abs(my) > 10) then
@@ -26,7 +17,6 @@
 
     local zoomFOV = Ternary(InputDown("mmb"), 45 , nil)
 
-
 	plane.camera.cameraX = plane.camera.cameraX - mx / (zoomFOV or 10)
 	plane.camera.cameraY = plane.camera.cameraY - my / (zoomFOV or 10)
 	plane.camera.cameraZ = plane.camera.cameraZ or 0
@@ -34,7 +24,6 @@
     if IsSimpleFlight() then
         plane.camera.cameraY = clamp(plane.camera.cameraY, -89, 89)
     end
-
 
     -- Lerp camera towards plane rot
     if auto_center_delay and TimerConsumed(timer_auto_center) then
@@ -53,14 +42,12 @@
 
     end
 
-
 	local cameraRot = QuatEuler(plane.camera.cameraY, plane.camera.cameraX, plane.camera.cameraZ)
 	local cameraT = Transform(VecAdd(GetBodyTransform(plane.body).pos, 5), cameraRot)
     local scale = 1
 
 	plane.camera.zoom = plane.camera.zoom - InputValue("mousewheel") * plane.camera.zoom/5
 	plane.camera.zoom = clamp(plane.camera.zoom, 1, 500) * scale
-
 
     local camAddHeight = 2
     if plane.model == 'ac130' then
@@ -76,7 +63,6 @@
 	SetCameraTransform(camera, zoomFOV)
 
 end
-
 
 function plane_Camera(plane)
 
@@ -96,7 +82,6 @@
     end
 
 end
-
 
 function plane_ChangeCamera()
 
@@ -123,4 +108,5 @@
 
 function camera_LerpToRot()
 
-end+end
+

```

---

# Migration Report: script\plane\plane_constructor.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\plane\plane_constructor.lua
+++ patched/script\plane\plane_constructor.lua
@@ -1,8 +1,7 @@
--- Build the plane data object (entities and properties)
+#version 2
 function createPlaneObject(ID)
 
     -- Default plane is a mig29
-
 
     local _vehicle = nil
 
@@ -12,7 +11,6 @@
             break
         end
     end
-
 
     local plane = {
 
@@ -41,7 +39,6 @@
             brakeImpulseAmt = 500,
             timeOfDeath = 0,
             groundDist = 0,
-
 
         -- weapons
             isArmed = true,
@@ -86,7 +83,6 @@
 
     }
 
-
     plane.weap = {
         weaponObjects = GetWeaponLocations(plane),
         secondary_lastIndex = 1
@@ -99,7 +95,6 @@
             special = {time = 0, rpm = 1200},
         }
     }
-
 
     plane.targetting = {
         target = 0,
@@ -120,14 +115,12 @@
         zoom = 20,
     }
 
-
     plane_UpdateProperties(plane)
     plane_CollectParts_Aero(plane)
     plane_ProcessHealth(plane)
     plane_ManageTargetting(plane)
     plane_SetMinAltitude(plane)
     plane_AutoConvertToPreset(plane)
-
 
     plane.landing_gear = {
         isDown = true,
@@ -143,14 +136,12 @@
         retract_timer = TimerCreateRPM(0, 60/2)
     }
 
-
     plane.exhausts = {}
     for index, light in ipairs(plane.AllLights) do
         if HasTag(light, "exhaust") then
             table.insert(plane.exhausts, light)
         end
     end
-
 
     -- No intercollisions, but leave world collision on.
     for _, shape in ipairs(plane.AllShapes) do
@@ -165,3 +156,4 @@
     return plane
 
 end
+

```

---

# Migration Report: script\plane\plane_functions.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\plane\plane_functions.lua
+++ patched/script\plane\plane_functions.lua
@@ -1,19 +1,7 @@
-FlightModes = {
-    simple = "simple",
-    simulation = "simulation",
-}
-
-InputControlIncrement = 0.05 -- Controls gradual steering impulse change.
-InputControls = { w = 0, a = 0, s = 0, d = 0, c = 0, z = 0, }
-
-
-
---PLANE
-
-    function plane_UpdateProperties(plane)
+#version 2
+function plane_UpdateProperties(plane)
 
         plane.isValid = plane_isValid(plane)
-
 
         plane.tr = GetBodyTransform(plane.body)
         plane.vel = GetBodyVelocity(plane.body)
@@ -23,10 +11,8 @@
         plane.totalVel = math.abs(plane.vel[1]) + math.abs(plane.vel[2]) + math.abs(plane.vel[3])
         plane.fwdVel = clamp(math.abs(plane.topSpeed / -plane.lvel[3]), 0, 100)
 
-
-        plane.playerInPlane = GetPlayerVehicle() == plane.vehicle
+        plane.playerInPlane = GetPlayerVehicle(playerId) == plane.vehicle
         plane.playerInUnbrokenPlane = plane.playerInPlane and plane.isAlive
-
 
         plane.forces = plane.forces or Vec(0,0,0)
         plane.speedFac = clamp(plane.speed, 1, plane.speed) / plane.topSpeed
@@ -37,8 +23,7 @@
 
     end
 
-    --- Accelerates towards the set thrust (simulates gradual engine wind up/down)
-    function plane_SetThrustOutput(plane)
+function plane_SetThrustOutput(plane)
         if plane.thrustOutput <= plane.thrust - 1 then
             plane.thrustOutput = plane.thrustOutput + plane.thrustAcc
         elseif plane.thrustOutput >= plane.thrust + 1 then
@@ -46,12 +31,11 @@
         end
     end
 
-    --- Sets thrust between 0 and 1
-    function plane_SetThrust(sign)
+function plane_SetThrust(sign)
         plane.thrust = plane.thrust + plane.thrustIncrement * sign
     end
 
-    function plane_ProcessHealth(plane)
+function plane_ProcessHealth(plane)
 
         plane.health = clamp(CompressRange(GetVehicleHealth(plane.vehicle), PLANE_DEAD_HEALTH, 1), 0, 1)
 
@@ -72,20 +56,19 @@
 
     end
 
-    function plane_ToggleEngine(plane)
-    end
-
-
-    function plane_RunPropellers()
+function plane_ToggleEngine(plane)
+    end
+
+function plane_RunPropellers()
         local propellers = FindJoints('planePropeller', true)
         for key, propeller in pairs(propellers) do
             SetJointMotor(propeller, 15)
         end
     end
 
-    function plane_Input(plane)
-
-        if GetPlayerVehicle() == plane.vehicle then
+function plane_Input(plane)
+
+        if GetPlayerVehicle(playerId) == plane.vehicle then
 
             if plane.isAlive then
 
@@ -119,7 +102,6 @@
 
             end
 
-
             if Config.debug then
 
                 if InputPressed("f1") then
@@ -146,10 +128,9 @@
 
         end
 
-
-    end
-
-    function plane_SetMinAltitude(plane)
+    end
+
+function plane_SetMinAltitude(plane)
         -- Lowest point ooint of the plane (light entity on the wheel)
         for index, light in ipairs(FindLights('ground', true)) do
             if GetBodyVehicle(GetShapeBody(GetLightShape(light))) == plane.vehicle then
@@ -161,11 +142,7 @@
         end
     end
 
-
-
---Effects
-
-    function plane_Sound(plane)
+function plane_Sound(plane)
 
         PlayLoop(sounds.fire_large, plane.tr.pos, 1 - plane.health + 0.25)
 
@@ -201,7 +178,7 @@
 
     end
 
-    function plane_VisualEffects(plane)
+function plane_VisualEffects(plane)
 
         for index, exhaust in pairs(plane.exhausts) do
 
@@ -212,7 +189,6 @@
 
             local rdmSmokeVec = VecScale(Vec(math.random() - 0.5, math.random() - 0.5, math.random() - 0.5), math.random(2, 5))
             particle_blackSmoke(VecAdd(plane.tr.pos, rdmSmokeVec), damageAlpha * 2, damageAlpha * 2)
-
 
             if plane.engineOn then
 
@@ -233,7 +209,6 @@
 
         end
 
-
         -- Spawn fire for a specified duration after death is triggered.
         if not plane.isAlive then
 
@@ -248,7 +223,6 @@
 
                 PlayLoop(sounds.fire_small, plane.tr.pos, fireSmall * fireVolumeScale)
                 PlayLoop(sounds.fire_large, plane.tr.pos, fireLarge * fireVolumeScale)
-
 
                 local amount = 1 - ((GetTime() / (endPlaneDeathTime)))
 
@@ -266,17 +240,14 @@
 
     end
 
-
---MISC
-
-    function plane_StateText(plane)
+function plane_StateText(plane)
         plane.status = "-"
         if InputDown("space") then
             plane_StatusAppend(plane, "Air-Braking")
         end
     end
 
-    function plane_CameraAimGroundSteering(plane)
+function plane_CameraAimGroundSteering(plane)
 
         local vTr = GetVehicleTransform(plane.tr)
         local camFwd = TransformToParentPoint(GetCameraTransform(), Vec(0, 0, -1))
@@ -288,26 +259,28 @@
 
     end
 
-    function plane_GetFwdPos(plane, distance)
+function plane_GetFwdPos(plane, distance)
         return TransformToParentPoint(GetBodyTransform(plane.body), Vec(0, 0, distance or -500))
     end
 
-    function plane_isValid(plane) return IsHandleValid(plane.body) and IsHandleValid(plane.vehicle) end
-
-    function plane_Delete(plane)
+function plane_isValid(plane) return IsHandleValid(plane.body) and IsHandleValid(plane.vehicle) end
+
+function plane_Delete(plane)
         plane.isValid = false
         for _, body in ipairs(plane.AllBodies) do
             Delete(body)
         end
     end
 
-    function VehicleIsPlane(vehicle) return PLANES_VEHICLES[vehicle] ~= nil end
-    function VehicleIsAlivePlane(vehicle) return VehicleIsPlane(vehicle) and GetVehicleHealth(vehicle) >= PLANE_DEAD_HEALTH end
-
-    function IsSimulationFlight() return FlightMode == FlightModes.simulation end
-    function IsSimpleFlight() return FlightMode == FlightModes.simple end
-
-    function Manage_SmallMapMode()
+function VehicleIsPlane(vehicle) return PLANES_VEHICLES[vehicle] ~= nil end
+
+function VehicleIsAlivePlane(vehicle) return VehicleIsPlane(vehicle) and GetVehicleHealth(vehicle) >= PLANE_DEAD_HEALTH end
+
+function IsSimulationFlight() return FlightMode == FlightModes.simulation end
+
+function IsSimpleFlight() return FlightMode == FlightModes.simple end
+
+function Manage_SmallMapMode()
 
         local smm = Config.smallMapMode
 
@@ -321,23 +294,18 @@
 
     end
 
-    function plane_IsVtolCapable(plane)
+function plane_IsVtolCapable(plane)
         return Ternary(#plane.parts.vtol >= 1, true, false)
     end
 
-    function plane_StatusAppend(plane, str)
+function plane_StatusAppend(plane, str)
         plane.status = string_append(plane.status, str)
     end
 
-    function plane_ProcessStatus()
-    end
-
-
-
-
---Weapons
-
-    function plane_ManageShooting(plane)
+function plane_ProcessStatus()
+    end
+
+function plane_ManageShooting(plane)
 
         if plane.isArmed then
 
@@ -368,7 +336,6 @@
                         -- Moves the aim pos just above where the crosshair (weapon body aligned) hits the world.
                         local shootTr = TransformCopy(weapTr)
 
-
                         local projPreset = ProjectilePresets.bullets.standard
                         if plane.model == 'a10' then
                             projPreset = ProjectilePresets.bullets.emg
@@ -376,7 +343,6 @@
 
                         -- Shoot projectile.
                         Projectiles_CreateProjectile(shootTr, Projectiles, projPreset, { plane.body })
-
 
                         ParticleReset()
                         ParticleType("smoke")
@@ -406,11 +372,9 @@
                         plane.weap.secondary_lastIndex = plane.weap.secondary_lastIndex + 1
                     end
 
-
                     local weapTr = GetLightTransform(plane.weap.weaponObjects.secondary[plane.weap.secondary_lastIndex].light)
                     local shootTr = TransformCopy(weapTr)
                     shootTr.rot = QuatLookAt(plTr.pos, TransformToParentPoint(plTr, Vec(0, 0, -300)))
-
 
                     if plane.model == "harrier" then
 
@@ -456,7 +420,6 @@
 
                     end
 
-
                 end
 
                 if InputDown('rmb') then
@@ -487,19 +450,8 @@
         TimerRunTime(plane.timers.weap.special)
 
     end
-    -- function plane_ChangeWeapon(plane)
-    --     -- if InputPressed("f") then
-    --     --     PlaySound(sounds.click, GetCameraTransform().pos, 1)
-    --     --     if plane.weapon ~= plane.weapons[#plane.weapons] then
-    --     --         -- plane.weapon = plane.weapons[]
-    --     --     else
-    --     --         plane.weapon = plane.weapons[1] -- loop to start
-    --     --     end
-    --     -- end
-    -- end
-
-
---DEBUG
-    function plane_Debug(plane)
-
-    end
+
+function plane_Debug(plane)
+
+    end
+

```

---

# Migration Report: script\plane\plane_hud.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\plane\plane_hud.lua
+++ patched/script\plane\plane_hud.lua
@@ -1,5 +1,4 @@
-
-
+#version 2
 function plane_draw_gyro(plane, uiW, uiH)
     do UiPush()
         drawUiGyro(plane, uiW, uiH)
@@ -16,7 +15,6 @@
 
 function plane_draw_hud(plane, uiW, uiH)
     do UiPush()
-
 
     local c = Vec(0.5,1,0.5)
     if plane.health <= 0 then c = Vec(1,0,0) end
@@ -37,7 +35,6 @@
 
     UiPop() end
 
-
     do UiPush()
 
         local w = 50
@@ -47,7 +44,6 @@
         UiImageBox("MOD/img/hud_crosshair_outer.png", w, w)
 
     UiPop() end
-
 
     do UiPush()
 
@@ -72,12 +68,9 @@
                 UiImageBox("MOD/img/dot.png", 15, 15, 0,0)
             end
 
-
         end
 
-
-    UiPop() end
-
+    UiPop() end
 
     if plane.playerInUnbrokenPlane then
 
@@ -149,7 +142,6 @@
 
     UiPop() end
 
-
     -- hud STATUS
     do UiPush()
         UiTranslate(960, 850)
@@ -171,7 +163,6 @@
         end
     UiPop() end
 
-
     do UiPush()
         UiAlign("left top")
         UiTranslate(UiCenter() +  uiW / 2, 0)
@@ -217,18 +208,12 @@
             UiColor(1, speedC, speedC)
             UiText(knots .. " Knots")
 
-
             UiTranslate(275, 25)
             plane_draw_Speed(plane)
 
         UiPop() end
 
-
-
-
-
-    UiPop() end
-
+    UiPop() end
 
     -- hud ALT
     do UiPush()
@@ -258,17 +243,15 @@
         UiAlign("center middle")
         UiTranslate(UiCenter() - uiW/2, 300)
 
-
         local colorVecs = {
             Vec(1, 0, 0),
             Vec(c[1], c[2], c[3]),
         }
 
-
         local frac = plane.health
 
         local a = 1
-        -- if plane.health <= 0.5 and plane.health > 0 then
+        -- if plane.health <= 0.5 and plane.health ~= 0 then
         --     a = Oscillate(1) + 1/2
         -- end
 
@@ -281,9 +264,7 @@
         UiColor(1,1,1, 1)
         UiText(sfn(frac * 100, 0) .. "%")
 
-
-    UiPop() end
-
+    UiPop() end
 
 UiPop() end
 
@@ -316,3 +297,4 @@
     UiImageBox("MOD/img/needle.png", 200,200, 0,0)
 
 end
+

```

---

# Migration Report: script\plane\plane_initializer.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\plane\plane_initializer.lua
+++ patched/script\plane\plane_initializer.lua
@@ -1,75 +1 @@
--- #include "../TDSU/tdsu.lua"
-
-
-
--- -- This script is ran for each plane that is spawned.
-
-
--- -- PLANE IDs
--- -- This script is responsible for processing plane parts and assigning a global ID to collection of parts.
--- -- In script.lua, the parts will be found using the assigned tags.
--- -- The unique ID is stored in the registry. It will be applied to the vehicle entity as a tag called ID and a value of an integer eg: ID=1, ID=6
-
-
--- function init()
-
---     -- Check whether the script instance is running.
---     CheckScriptEnabled()
-
-
---     -- Tag name.
---     IDTag = "Plane_ID"
-
---     -- This int can always be used as the current ID.
---     ID = GetString("level.Plane_ID")
---     if ID == "" then
---         ID = 0
---     end
---     SetString("level.Plane_ID", tonumber(ID) + 1)
-
-
---     -- Apply IDs
---     ApplyPlaneEntityIDs(ID)
-
--- end
-
-
--- function tick()
-
--- end
-
-
--- function ApplyPlaneEntityIDs(ID)
-
---     AllEntities = {
---         AllVehicles  = FindVehicles("", false),
---         AllBodies    = FindBodies("", false),
---         AllShapes    = FindShapes("", false),
---         AllLights    = FindLights("", false),
---         AllLocations = FindLocations("", false),
---         AllTriggers  = FindTriggers("", false),
---     }
-
---     for _, entity_group in pairs(AllEntities) do
---         for _, entity in ipairs(entity_group) do
---             SetTag(entity, IDTag, ID)
---         end
---     end
-
---     for index, shape in ipairs(AllEntities.AllShapes) do
---         SetShapeCollisionFilter(shape, 3, 1)
---     end
-
-
--- end
-
-
--- function CheckScriptEnabled()
-
---     if GetBool('level.planeScriptActive') == false then
---         Spawn('MOD/prefab/script.xml', Transform())
---         SetBool('level.planeScriptActive', true)
---         print("Created script.lua")
---     end
-
--- end
+#version 2

```

---

# Migration Report: script\plane\plane_physics.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\plane\plane_physics.lua
+++ patched/script\plane\plane_physics.lua
@@ -1,4 +1,4 @@
--- Apply engine/thrust impulse to move the plane forward.
+#version 2
 function plane_Move(plane)
 
     plane_SetThrustOutput(plane)
@@ -16,7 +16,6 @@
 
         elseif plane.speed < plane.topSpeed then
 
-
             if #plane.exhausts >= 1 then
 
                 local exhaust_count = #plane.exhausts
@@ -53,8 +52,6 @@
 
 end
 
-
--- Apply aerodynamic impulses.
 function plane_ApplyAerodynamics(plane)
 
     if plane.totalVel < 1 then
@@ -75,7 +72,6 @@
     force_x = GetRollAoA(plane.tr, plane.vel) / FwdVel / 2
     force_y = GetPitchAoA(plane.tr, plane.vel) / FwdVel
     force_z = GetYawAoA(plane.tr, plane.vel) / FwdVel / 4
-
 
     local impMult = 2
 
@@ -91,7 +87,6 @@
 
     local impSpeedScale = 1 - (plane.speedFac / plane.topSpeed)
     local imp = GTZero(GetBodyMass(plane.body) * impSpeedScale) * 5 * impMult
-
 
     dbw("AERO X", sfn(x))
     dbw("AERO Y", sfn(y))
@@ -102,7 +97,6 @@
     dbw("AERO LVEL", localVel)
     dbw("AERO IMP", imp)
 
-
     ApplyBodyImpulse(plane.body,
         plane.tr.pos,
         TransformToParentPoint(plane.tr, VecScale(Vec(force_x, 0, 0), imp)))
@@ -116,20 +110,16 @@
         TransformToParentPoint(plane.tr, VecScale(Vec(0, 1, 0))),
         TransformToParentPoint(plane.tr, VecScale(Vec(force_z, 0, 0), imp)))
 
-
     local angDim = 1 - (plane.speedFac / plane.topSpeed * 6)
     angDim = clamp(angDim, 0, 1)
     SetBodyAngularVelocity(plane.body, VecScale(GetBodyAngularVelocity(plane.body), angDim)) -- Diminish ang vel
 
-
     if Config.debug and plane.totalVel > 2 then
         plane_draw_Forces(plane, x, y, z, 5, 20)
     end
 
 end
 
-
--- Apply turbulence based on velocity and aerodynamics.
 function plane_ApplyTurbulence(plane)
 
     -- local turbImp = VecRdm(math.abs(plane.lvel[1] + plane.lvel[2]) * 10000)
@@ -146,11 +136,8 @@
     -- dbw("TURB imp", turbImp)
     -- dbw("TURBULENCE", TURBULENCE)
 
-
-end
-
-
--- Apply impulses to control the pitch, roll and yaw.
+end
+
 function plane_Steer(plane)
 
     local idealSpeedFactor = plane.idealSpeedFactor
@@ -177,7 +164,6 @@
 
     local ic = InputControls
     local inc = InputControlIncrement
-
 
     local w = InputDown("w")
     local s = InputDown("s")
@@ -185,7 +171,6 @@
     local d = InputDown("d")
     local c = InputDown("c")
     local z = InputDown("z")
-
 
     -- if camPos == "aligned" then
 
@@ -208,7 +193,6 @@
 
     -- end
 
-
     if w then
         ic.w = clamp(ic.w + inc, 0, 1)
         ApplyBodyImpulse(plane.body, nose, VecScale(planeUp, -imp * ic.w))
@@ -222,7 +206,6 @@
         ic.s = clamp(ic.s - inc, 0, 1)
     end
 
-
     if a then
         ic.a = clamp(ic.a + inc, 0, 1)
         ApplyBodyImpulse(plane.body, wing, VecScale(planeUp, -imp * ic.a * plane.rollVal))
@@ -236,7 +219,6 @@
         ic.d = clamp(ic.d - inc, 0, 1)
     end
 
-
     if z then
         ic.c = clamp(ic.c + inc, 0, 1)
         ApplyBodyImpulse(plane.body, nose, VecScale(planeLeft, -imp * ic.c))
@@ -250,14 +232,12 @@
         ic.z = clamp(ic.z - inc, 0, 1)
     end
 
-
     if InputDown("shift") and plane.thrust + plane.thrustIncrement <= 101 then
         plane.thrust = plane.thrust + 1
     end
     if InputDown("ctrl") and plane.thrust - plane.thrustIncrement >= 0 then
         plane.thrust = plane.thrust - 1
     end
-
 
     if InputDown("space") then
         ApplyBodyImpulse(
@@ -270,8 +250,6 @@
 
 end
 
-
--- Draw aerodynamic forces debug lines.
 function plane_draw_Forces(plane, x, y, z, outness, scale)
 
     local outness = outness or 5
@@ -310,9 +288,6 @@
 
 end
 
-
-
-
 function GetPitchAoA(tr, vel)
 
     local lVel = TransformToLocalVec(tr, vel)
@@ -348,3 +323,4 @@
     return aoa
 
 end
+

```

---

# Migration Report: script\plane\plane_physics_simple.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\plane\plane_physics_simple.lua
+++ patched/script\plane\plane_physics_simple.lua
@@ -1,4 +1,4 @@
--- Steer plane based on camera direction.
+#version 2
 function plane_Steer_Simple(plane, rot, disable_input)
 
     local pTr = TransformCopy(plane.tr)
@@ -14,7 +14,6 @@
     if speedClamped > plane.topSpeed /2 then
         turnAmt = math.abs(1 / turnDiv)
     end
-
 
     if not disable_input then
 
@@ -53,14 +52,12 @@
         end
     end
 
-
     local steerMult = 1
     if IsSimpleFlight() then
         if Config.smallMapMode then
             steerMult = 2
         end
     end
-
 
     local crosshairRot = rot or QuatLookAt(plane.tr.pos, crosshairPos)
 
@@ -90,12 +87,10 @@
         rollAmt[1] = rollAmt[1] * turnAmt * -350 / (plane.rollVal or 1)
         pTr.rot = QuatRotateQuat(pTr.rot, QuatEuler(0, 0, rollAmt[1]))
 
-
         -- -- Smooth roll
         -- plane.rotSOS = AutoSM_DefineQuat(pTrCopy.rot, 0, 0.5, 0)
         -- AutoSM_Update(plane.rotSOS, pTr.rot, GetTimeStep())
         -- pTr.rot = AutoSM_Get(plane.rotSOS)
-
 
         -- Align with crosshair pos
         pTr.rot = MakeQuaternion(QuatCopy(pTr.rot))
@@ -109,8 +104,6 @@
 
 end
 
-
--- Apply engine/thrust impulse to move the plane forward.
 function plane_Move_Simple(plane)
 
     local speed = plane.speed
@@ -134,7 +127,6 @@
     end
 
 end
-
 
 function plane_GetForwardVelAngle_old(plane)
     -- - Returns the angle between the plane's direction and velocity
@@ -161,7 +153,6 @@
     return angle
 end
 
-
 function plane_getLiftSpeedFac(plane)
     local x = plane.speed
     local b = plane.speed/3
@@ -170,4 +161,5 @@
         result = x
     end
     return result
-end+end
+

```

---

# Migration Report: script\plane\plane_presets.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\plane\plane_presets.lua
+++ patched/script\plane\plane_presets.lua
@@ -1,3 +1,4 @@
+#version 2
 function plane_AutoConvertToPreset(plane)
 
     if plane.model == "spitfire" then
@@ -20,7 +21,6 @@
 
 end
 
-
 function convertPlaneToSpitfire(plane)
     plane.topSpeed = 70
     plane.thrustImpulseAmount = 20
@@ -39,7 +39,6 @@
     plane.targetting.homingCapable = false
 
 end
-
 
 function convertPlaneToA10(plane)
     plane.topSpeed = 130
@@ -64,7 +63,6 @@
     }
 
 end
-
 
 function convertPlaneToBombardierJet(plane)
     plane.isArmed = false
@@ -145,6 +143,7 @@
     plane.yawFac = 1
 
 end
+
 function convertPlaneToHarrier(plane)
     plane.isArmed = true
 
@@ -168,4 +167,5 @@
 
     plane.targetting.homingCapable = false
 
-end+end
+

```

---

# Migration Report: script\plane\plane_targetting.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\plane\plane_targetting.lua
+++ patched/script\plane\plane_targetting.lua
@@ -1,3 +1,4 @@
+#version 2
 function plane_ManageTargetting(plane)
 
     local camTr = GetCameraTransform()
@@ -21,7 +22,6 @@
 
         end
     end
-
 
     -- dbw('#targetVehicles', #plane.targetting.targetVehicles)
 
@@ -72,8 +72,6 @@
 
 end
 
-
---- Change target to a random vehicle in table v.
 function changeTarget(plane, v)
     plane.targetting.target = GetRandomIndexValue(v)
     TimerResetTime(plane.targetting.lock.timer)
@@ -81,7 +79,6 @@
     plane.targetting.lock.locking = false
 end
 
-
 function plane_CheckTargetLocked(plane)
 
     if plane.targetting.lock.enabled and plane.targetting.homingCapable then
@@ -117,7 +114,6 @@
             plane.targetting.lock.locking = false
             plane.targetting.lock.locked = false
             plane.targetting.targetShape = nil
-
 
         end
         dbw('Target timer', plane.targetting.lock.timer.time)
@@ -130,7 +126,6 @@
 
 end
 
-
 function plane_draw_Targetting(plane)
     if #plane.targetting.targetVehicles >= 1 then
 
@@ -146,8 +141,6 @@
     end
 end
 
-
---- Draw a single target.
 function plane_draw_Target(plane, vehicle)
     do UiPush()
 
@@ -172,7 +165,6 @@
                     UiText(sfn(distToTarget) .. ' KM')
                 UiPop()
 
-
                 local c = Oscillate(0.9)
                 if plane.targetting.lock.locked then
 
@@ -206,3 +198,4 @@
 
     UiPop() end
 end
+

```

---

# Migration Report: script\plane\PLANES_manage.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\plane\PLANES_manage.lua
+++ patched/script\plane\PLANES_manage.lua
@@ -1,3 +1,4 @@
+#version 2
 function Init_PLANES()
 end
 
@@ -17,7 +18,6 @@
             plane_UpdateProperties(plane)
             plane_Input(plane)
 
-
             -- Plane move.
             if plane.isAlive then
 
@@ -27,13 +27,11 @@
 
             end
 
-
             plane_VisualEffects(plane)
             plane_Sound(plane)
 
-
             -- Player in plane.
-            if GetPlayerVehicle() == plane.vehicle then
+            if GetPlayerVehicle(playerId) == plane.vehicle then
 
                 crosshairPos = GetCrosshairWorldPos(plane.AllBodies, true, plane.tr.pos)
 
@@ -71,8 +69,7 @@
                         plane_Debug(plane)
                     end
 
-
-                    SetPlayerHealth(1)
+                    SetPlayerHealth(playerId, 1)
 
                 end
 
@@ -88,7 +85,7 @@
 
         if plane.isValid then
 
-            if GetPlayerVehicle() == plane.vehicle then
+            if GetPlayerVehicle(playerId) == plane.vehicle then
 
                 plane_Animate_AeroParts(plane)
 
@@ -113,7 +110,6 @@
         local uiW = 600
         local uiH = 650
 
-
         if ShouldDrawIngameOptions then
 
             DrawIngameOptions()
@@ -137,7 +133,7 @@
 
                     if plane.isValid then
 
-                        if GetPlayerVehicle() == plane.vehicle then
+                        if GetPlayerVehicle(playerId) == plane.vehicle then
 
                             plane_draw_hud(plane, uiW + 200, uiH)
 
@@ -160,3 +156,4 @@
 
     UiPop()
 end
+

```

---

# Migration Report: script\projectiles.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\projectiles.lua
+++ patched/script\projectiles.lua
@@ -1,6 +1,4 @@
-Projectiles = {}
-
-
+#version 2
 function Init_Projectiles()
 
     ProjectilePresets = {
@@ -383,7 +381,6 @@
     proj.vel = VecSub(proj.transform.pos, proj.transformLast.pos)
     -- proj.lifeRemaining = (proj.lifeLength + proj.lifeStart) - proj.lifeStart
 
-
     proj.lifeLength = proj.lifeLength - GetTimeStep()
     if proj.lifeLength <= 0 then
         proj.hit = true
@@ -406,7 +403,7 @@
         --+ Hit Action
         -- ApplyBodyImpulse(GetShapeBody(hitShape), hitPos, VecScale(QuatToDir(proj.transform.rot), proj.force))
 
-        if proj.explosionSize > 0 then
+        if proj.explosionSize ~= 0 then
             Explosion(hitPos, proj.explosionSize)
         end
 
@@ -434,14 +431,12 @@
         proj.isActive = true
     end
 
-
     --+ Proj homing.
     if proj.homing.max > 0 and proj.homing.targetShape ~= nil then
 
         local targetBodyTr = GetBodyTransform(GetShapeBody(proj.homing.targetShape))
         local targetPos = TransformToParentPoint(targetBodyTr, proj.homing.targetBodyRelPos)
         local targetVel = GetBodyVelocity(GetShapeBody(proj.homing.targetShape))
-
 
         dbl(proj.transform.pos, targetPos, 1,0,0, 0.5)
         dbcr(targetPos, 1,0,0, 1)
@@ -458,13 +453,11 @@
         proj.transform.rot = MakeQuaternion(proj.transform.rot)
         proj.transform.rot = proj.transform.rot:Approach(QuatLookAt(proj.transform.pos, targetPos), proj.homing.force) -- Rotate towards homing target.
 
-
         if proj.homing.force < proj.homing.max then -- Increment homing strength.
             proj.homing.force = proj.homing.force + proj.homing.gain
         end
 
     end
-
 
     --+ Draw sprite
     if proj.effects.sprite_facePlayer then
@@ -474,7 +467,6 @@
         DrawSprite(LoadSprite(proj.effects.sprite), Transform(proj.transform.pos, QuatRotateQuat(proj.transform.rot, QuatEuler(0,-math.random(88,92),0))), proj.effects.sprite_dimensions[1], proj.effects.sprite_dimensions[2], 1, 1, 1, 1, true)
     end
 
-
     --+ Particles
     if proj.category == 'missile' then
         particle_missileSmoke(proj.transform, proj.speed)
@@ -482,7 +474,6 @@
         particle_rocketSmoke(proj.transform, proj.speed)
     end
 
-
     local c = proj.effects.color
     PointLight(proj.transform.pos, c[1], c[2], c[3], math.random()+1)
 
@@ -527,60 +518,6 @@
     UiPop()
 end
 
--- -- Calculates the 3D proportional navigation guidance command
--- -- target_pos: table representing the target position with fields x, y, and z
--- -- target_vel: table representing the target velocity with fields x, y, and z
--- -- own_pos: table representing the ownship position with fields x, y, and z
--- -- own_vel: table representing the ownship velocity with fields x, y, and z
--- -- time_to_impact: estimated time to impact in seconds
--- function proportional_navigation_guidance_3d(target_pos, target_vel, own_pos, own_vel, time_to_impact)
-
---     local rel_pos = Vec(
---         target_pos[1] - own_pos[1],
---         target_pos[2] - own_pos[2],
---         target_pos[3] - own_pos[3])
-
---     local rel_vel = Vec(
---         target_vel[1] - own_vel[1],
---         target_vel[2] - own_vel[2],
---         target_vel[3] - own_vel[3])
-
---     -- Calculate magnitude of relative position and velocity vectors
---     local range = math.sqrt(rel_pos[1] ^ 2 + rel_pos[2] ^ 2 + rel_pos[3] ^ 2)
---     local closing_speed = (rel_pos[1] * rel_vel[1] + rel_pos[2] * rel_vel[2] + rel_pos[3] * rel_vel[3]) / range
-
---     -- Check for divide by zero
---     if closing_speed == 0 then
---         return Vec(0, 0, 0)
---     end
-
---     -- Calculate proportional gain and navigation constant
---     local proportional_gain = 3 / time_to_impact -- Proportional gain
---     local gamma = proportional_gain / closing_speed -- Navigation constant
-
---     -- Calculate navigation command
---     local vel_perp = Vec(
---         rel_vel[2] * rel_pos[3] - rel_vel[3] * rel_pos[2],
---         rel_vel[3] * rel_pos[1] - rel_vel[1] * rel_pos[3],
---         rel_vel[1] * rel_pos[2] - rel_vel[2] * rel_pos[1])
-
---     local vel_perp_mag = math.sqrt(vel_perp[1] ^ 2 + vel_perp[2] ^ 2 + vel_perp[3] ^ 2)
---     local guidance = Vec(
---         gamma * vel_perp[1] / vel_perp_mag,
---         gamma * vel_perp[2] / vel_perp_mag,
---         gamma * vel_perp[3] / vel_perp_mag)
-
---     return guidance
-
--- end
-
-
--- Calculates the 3D proportional navigation desired direction
--- target_pos: table representing the target position with fields x, y, and z
--- target_vel: table representing the target velocity with fields x, y, and z
--- own_pos: table representing the ownship position with fields x, y, and z
--- own_vel: table representing the ownship velocity with fields x, y, and z
--- time_to_impact: estimated time to impact in seconds
 function proportional_navigation_direction_3d(target_pos, target_vel, own_pos, own_vel, time_to_impact)
     local rel_pos = { target_pos[1] - own_pos[1], target_pos[2] - own_pos[2], target_pos[3] - own_pos[3] }
     local rel_vel = { target_vel[1] - own_vel[1], target_vel[2] - own_vel[2], target_vel[3] - own_vel[3] }
@@ -607,11 +544,12 @@
   
     -- Normalize direction vector
     local direction_mag = math.sqrt(direction[1]^2 + direction[2]^2 + direction[3]^2)
-    if direction_mag > 0 then
+    if direction_mag ~= 0 then
       direction[1] = direction[1] / direction_mag
       direction[2] = direction[2] / direction_mag
       direction[3] = direction[3] / direction_mag
     end
   
     return direction
-  end+  end
+

```

---

# Migration Report: script\registry.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\registry.lua
+++ patched/script\registry.lua
@@ -1,7 +1,7 @@
+#version 2
 local versions = {
     1,2,3,4,5,
 }
-
 
 function CheckRegInitialized()
 
@@ -9,12 +9,11 @@
 
     if version < versions[#versions] then
         ClearKey("savegame.mod")
-        SetInt("savegame.mod.version", versions[#versions])
+        SetInt("savegame.mod.version", versions[#versions], true)
         print("Reg reset version")
     end
 
 end
-
 
 function Init_Config()
 
@@ -40,3 +39,4 @@
     })
 
 end
+

```

---

# Migration Report: script\sounds.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\sounds.lua
+++ patched/script\sounds.lua
@@ -1,3 +1,4 @@
+#version 2
 function Init_Sounds()
     sounds = {
 
@@ -16,7 +17,6 @@
         prop_3 = LoadLoop("MOD/snd/prop_3-5.ogg"),
         prop_4 = LoadLoop("MOD/snd/prop_4-5.ogg"),
         prop_5 = LoadLoop("MOD/snd/prop_5-5.ogg"),
-
 
         -- jet engine
         jet_engine_loop_mig29 = LoadLoop("MOD/snd/jet_engine_loop_mig29.ogg"),
@@ -41,8 +41,6 @@
 
     }
 
-
-
     loops = {
 
         landing_gear = LoadLoop("MOD/snd/loop_landing_gear.ogg"),
@@ -62,4 +60,5 @@
         table.insert(sounds, LoadSound(path .. i .. ".ogg"))
     end
     return sounds
-end+end
+

```

---

# Migration Report: script\starting_plane.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\starting_plane.lua
+++ patched/script\starting_plane.lua
@@ -1,4 +1,6 @@
-function init()
+#version 2
+function server.init()
     local plane = FindVehicle("")
-    SetPlayerVehicle(plane)
-end+    SetPlayerVehicle(playerId, plane)
+end
+

```

---

# Migration Report: script\ui\ui.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\ui\ui.lua
+++ patched/script\ui\ui.lua
@@ -1,7 +1,4 @@
-scrolly = 0
-scrolly_presets = 0
-
---- Draw the pane containing the list of items.
+#version 2
 function drawItemListMenu()
 
     local listH = 50
@@ -38,7 +35,6 @@
 
 end
 
--- Draw a single item in the list of items.
 function uiList_Item(text, itemChainIndex, item, listH)
     do UiPush()
 
@@ -98,7 +94,6 @@
             r,g,b = Oscillate(1.5)/2 + 0.5, 0.25, 0.25
         end
 
-
         do UiPush()
             -- Button base
             UiButtonImageBox('ui/common/box-solid-6.png', 10,10, r,g,b, a)
@@ -106,7 +101,6 @@
                 UI_SELECTED_ITEM = itemChainIndex -- Changed selected ui item
             end
         end UiPop()
-
 
         -- Left side
         do UiPush()
@@ -135,7 +129,6 @@
                 UiImageBox('MOD/img/icon_event.png', bw * 1.25, bh * 1.25, 0,0)
             end
 
-
             UiAlign('left middle')
             margin(bw*1.5, 0)
             UiText(item.item.type)
@@ -145,7 +138,6 @@
 
         end UiPop()
 
-
         -- Button: Delete item
         do UiPush()
 
@@ -174,12 +166,11 @@
                     local tr = TransformCopy(ITEM_CHAIN[UI_SELECTED_ITEM].item.tr)
                     tr.pos = VecSub(tr.pos, playerRelCamPos) -- Compensate for player tr to cam tr
 
-                    SetPlayerTransform(tr)
+                    SetPlayerTransform(playerId, tr)
                 end
             end
 
         end UiPop()
-
 
         -- Buttons: Reorder
         do UiPush()
@@ -217,7 +208,6 @@
     end UiPop()
 end
 
--- Dynamic buttons.
 function uiList_dynamicButtons(w,h, index)
     do UiPush()
 
@@ -253,7 +243,6 @@
     end UiPop()
 end
 
--- Add item.
 function uiList_addItem(index)
     do UiPush()
 
@@ -270,7 +259,6 @@
     end UiPop()
 end
 
--- Duplicate item.
 function uiList_duplicateItem(index)
     do UiPush()
 
@@ -298,7 +286,6 @@
 
         local control = UiControls[i]
 
-
         UiColor(0,0,0, 0.5)
         UiButtonImageBox('ui/common/box-solid-6.png', 10,10, 0,0,0, 0.5)
         UiButtonHoverColor(0,0,0, 0.5)
@@ -306,7 +293,6 @@
             _G[control.func]()
         end
 
-
         UiColor(0,0,0, 0.5)
         if _G[control.bool] then
             UiColor(0,1,0, 0.5)
@@ -318,7 +304,6 @@
                 UiImageBox('ui/common/box-outline-6.png', w-m, rectH-m, 10,10)
             end
         UiPop() end
-
 
         do UiPush()
 
@@ -349,3 +334,4 @@
     end
 
 end
+

```

---

# Migration Report: script\ui\ui_compass.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\ui\ui_compass.lua
+++ patched/script\ui\ui_compass.lua
@@ -1,3 +1,4 @@
+#version 2
 function drawCompass(plane, uiW, uiH)
 
     UiTextShadow(0,0,0,0, 0,0)
@@ -21,14 +22,11 @@
     UiFont('bold.ttf', 20)
     UiColor(1,1,1, 1)
 
-
     do UiPush()
         UiColor(0,0,0, 0.5)
         UiTranslate(0, 30)
         UiRect(4, 10)
     UiPop() end
-
-
 
     local camTr = GetCameraTransform()
     -- local camTr = plane.tr
@@ -57,7 +55,6 @@
 
     UiTranslate(UiCenter(), UiMiddle())
 
-
     UiAlign('center middle')
     UiFont('bold.ttf', 20)
     UiTextShadow(0,0,0,0, 0,0)
@@ -67,8 +64,6 @@
 
     UiWindow(width, height, true)
     UiTranslate(UiCenter(), UiMiddle())
-
-
 
     UiColor(0,0,0, 0.5)
     do UiPush()
@@ -82,13 +77,11 @@
         UiRect(120, 6)
     UiPop() end
 
-
     -- local camTr = GetCameraTransform()
     local camTr = plane.tr
     local camDir = QuatToDir(camTr.rot)
     local camDirY = math.deg(camDir[2]) * math.pi / 2
     -- dbw('camDirY', camDirY)
-
 
     local s = 1
 
@@ -99,7 +92,6 @@
     local y = UiHeight() / points / s
 
     UiColor(1,1,1, 1)
-
 
     for i = 0, points do
         do UiPush()
@@ -123,7 +115,6 @@
                 drawText = true
             end
 
-
             drawGyroValue(1, val, width, w, y, drawText, lineH)
             drawGyroValue(-1, val, width, w, y, drawText, lineH)
 
@@ -131,7 +122,6 @@
     end
 
 end
-
 
 function drawGyroValue(sign, val, width, w, y, drawText, lineH)
 
@@ -162,3 +152,4 @@
 
     UiPop() end
 end
+

```

---

# Migration Report: script\ui\ui_draw.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\ui\ui_draw.lua
+++ patched/script\ui\ui_draw.lua
@@ -1,3 +1,4 @@
+#version 2
 function Init_Draw()
     Controls = {
 
@@ -54,7 +55,6 @@
                         simulation  = "Mouse wheel"},
 
         { title = "" },
-
 
             { title = "Engine ON/OFF",
                         simple      = "N",
@@ -80,7 +80,6 @@
     end
 
 end
-
 
 function Draw_WriteMessage(message, fontSize)
     UiPush()
@@ -221,7 +220,6 @@
         UiTranslate(0, -fs)
         UiTranslate(0, -fs)
 
-
         UiText('Yaw = Z/C')
         UiTranslate(0, -fs)
         UiText('Pitch = W/S')
@@ -249,3 +247,4 @@
 
     UiPop()
 end
+

```

---

# Migration Report: script\ui\ui_options.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\ui\ui_options.lua
+++ patched/script\ui\ui_options.lua
@@ -1,3 +1,4 @@
+#version 2
 function DrawIngameOptions()
 
     UiMakeInteractive()
@@ -13,15 +14,12 @@
     local marginY = 20
     local marginY2 = marginY*1.25
 
-
-
     margin(UiCenter()/2, UiMiddle()/4)
     UiPush()
         UiColor(0,0,0, 0.8)
         UiAlign("left top")
         UiRect(w, h)
     UiPop()
-
 
     -- Title
     margin(w_center, 0)
@@ -31,7 +29,6 @@
         UiAlign("center bottom")
         UiText("Options")
     UiPop()
-
 
     -- Close button
     UiPush()
@@ -70,7 +67,7 @@
         UiAlign('center middle')
         UiButtonImageBox('ui/common/box-outline-6.png', 10,10, c[1], c[2], c[3], 1)
         if UiTextButton('Simulation', btn_w, marginY2*1.5) then
-            SetString("savegame.mod.FlightMode", FlightModes.simulation)
+            SetString("savegame.mod.FlightMode", FlightModes.simulation, true)
         end
     UiPop()
 
@@ -81,7 +78,7 @@
         UiAlign('center middle')
         UiButtonImageBox('ui/common/box-outline-6.png', 10,10, c[1], c[2], c[3], 1)
         if UiTextButton('Simple', btn_w, marginY2*1.5) then
-            SetString("savegame.mod.FlightMode", FlightModes.simple)
+            SetString("savegame.mod.FlightMode", FlightModes.simple, true)
         end
     UiPop()
 
@@ -106,7 +103,6 @@
 
     end
 
-
     margin(0, marginY2*2)
     margin(0, marginY2*2)
 
@@ -152,7 +148,7 @@
         UiAlign('center middle')
         UiButtonImageBox('ui/common/box-outline-6.png', 10,10, c[1], c[2], c[3], 1)
         if UiTextButton('Ground Enemy AI', btn_w, marginY2*1.5) then
-            SetBool("savegame.mod.enemies_enabled", not GetBool("savegame.mod.enemies_enabled"))
+            SetBool("savegame.mod.enemies_enabled", not GetBool("savegame.mod.enemies_enabled"), true)
         end
     UiPop()
 
@@ -216,4 +212,5 @@
     else
         return Vec(0.75,0.75,0.75)
     end
-end+end
+

```

---

# Migration Report: script\ui\ui_textBinding.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\ui\ui_textBinding.lua
+++ patched/script\ui\ui_textBinding.lua
@@ -1,23 +1,16 @@
-activeAssignment = false
-activeNameAssignment = false
-activeTable = {tb = '', key = ''}
-lastKeyPressed = ''
-font_size = 28
-
-backspaceTimer = 0
-
-
+#version 2
 function isActiveTableKey(tb, key) return tb == activeTable.tb and activeTable.key == key end
+
 function resetActiveTable() activeTable = {tb = '', key = ''} end
 
 function enableTextField(tb, key)
     activeNameAssignment = true
     activeTable = {tb = tb, key = key}
 end
+
 function disableTextField()
     activeNameAssignment = false
 end
-
 
 function uiTextField(w, h, tb, key)
 
@@ -194,18 +187,14 @@
             UiImageBox('MOD/img/icon_plus.png', h/2, h/2)
         end
 
-
-    UiPop() end
-end
-
---- Manage keybinds and textfields.
+    UiPop() end
+end
+
 function ManageUiBinding()
 
     local bindTriggered = false
 
-
     lastKeyPressed = string.lower(InputLastPressedKey())
-
 
     -- Manage keybinding.
     if activeAssignment and isKeyValid(lastKeyPressed) then
@@ -261,18 +250,3 @@
 
 end
 
-
--- function uiBinding_backspaceTimer()
-
---     TimerRunTime(backspaceTimer)
-
---     if TimerConsumed(backspaceTimer) then
---         TimerResetTime(backspaceTimer)
-
---         return true
-
---     end
-
---     return false
-
--- end

```

---

# Migration Report: script\ui\ui_tools.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\ui\ui_tools.lua
+++ patched/script\ui\ui_tools.lua
@@ -1,3 +1,4 @@
+#version 2
 function margin(x,y) UiTranslate(x,y) end
 
 function drawSquare()
@@ -32,12 +33,10 @@
     UiColor(1,1,1, 1)
 end
 
--- Draw the outline and highlight of a shape
 function drawShape(s)
     DrawShapeOutline(s, 1,1,1, 1)
     DrawShapeHighlight(s, 0.25)
 end
-
 
 function createSlider(title, tb, key, valueText, min, max, w, h, fs)
 
@@ -105,3 +104,4 @@
     end
 
 end
+

```

---

# Migration Report: script\weapons.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\weapons.lua
+++ patched/script\weapons.lua
@@ -1,3 +1,4 @@
+#version 2
 function GetWeaponLocations(plane)
 
     -- Find lights
@@ -5,13 +6,11 @@
     local lights_weap_secondary = FindLights('weap_secondary', true)
     local lights_weap_special = FindLights('weap_special', true)
 
-
     local weaponObjects = {
         primary = {},
         secondary = {},
         special = {},
     }
-
 
     for key, light in pairs(lights_weap_primary) do
 
@@ -56,7 +55,6 @@
 
 end
 
---- Returns the light, its shape and body.
 function getLightObject(light)
 
     local l = {}
@@ -70,3 +68,4 @@
     return l
 
 end
+

```

---

# Migration Report: script.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script.lua
+++ patched/script.lua
@@ -1,128 +1,4 @@
-#include "Automatic.lua"
-#include "TDSU/tdsu.lua"
-#include "script/ai_SAMS.lua"
-#include "script/ai_planes.lua"
-#include "script/debug.lua"
-#include "script/input/controlPanel.lua"
-#include "script/input/input.lua"
-#include "script/input/keybinds.lua"
-#include "script/particles.lua"
-#include "script/plane/plane_animate.lua"
-#include "script/plane/plane_builder.lua"
-#include "script/plane/plane_camera.lua"
-#include "script/plane/plane_constructor.lua"
-#include "script/plane/plane_functions.lua"
-#include "script/plane/plane_hud.lua"
-#include "script/plane/plane_targetting.lua"
-#include "script/plane/plane_physics.lua"
-#include "script/plane/plane_physics_simple.lua"
-#include "script/plane/plane_presets.lua"
-#include "script/plane/planes_manage.lua"
-#include "script/projectiles.lua"
-#include "script/registry.lua"
-#include "script/sounds.lua"
-#include "script/ui/ui.lua"
-#include "script/ui/ui_compass.lua"
-#include "script/ui/ui_draw.lua"
-#include "script/ui/ui_options.lua"
-#include "script/ui/ui_textBinding.lua"
-#include "script/ui/ui_tools.lua"
-#include "script/weapons.lua"
-
-
-
-
-PLANES = {} -- plane objects.
-PLANES_VEHICLES = {} -- Find plane object by vehicle id
-
-ShouldDrawIngameOptions = false
-PLANE_DEAD_HEALTH = 0.6
-
-
-
-function init()
-
-    Init_Utils()
-
-    Init_PLANES()
-    Init_AIPLANES()
-    Init_Config()
-    Init_Sounds()
-    Init_Projectiles()
-    Init_Enemies()
-    Init_Draw()
-    Manage_SmallMapMode()
-
-
-    SelectedCamera = CameraPositions[1]
-
-    SetString("hud.notification", "Note: The F-15 landing gear system is still in development.")
-
-end
-
-function tick()
-
-    Tick_Utils()
-
-    AllVehicles = FindVehicles("", true)
-
-    FlightMode = GetString("savegame.mod.FlightMode")
-    FlightModeSet = GetBool("savegame.mod.flightmodeset")
-
-    if not FlightModeSet then
-        SetString("savegame.mod.FlightMode", FlightModes.simple)
-        SetBool("savegame.mod.flightmodeset", true)
-        print("backup flightmode simple")
-    end
-
-    dbw("PlayerInPlane", PlayerInPlane)
-
-    if PlayerInPlane and InputPressed(Config.toggleOptions) then
-
-        ShouldDrawIngameOptions = not ShouldDrawIngameOptions
-        SetBool("level.showedOptions", true)
-
-    elseif not PlayerInPlane then
-
-        ShouldDrawIngameOptions = false
-
-    end
-
-
-    -- Root of plane management.
-    Tick_PLANES()
-
-    Tick_aiplanes()
-    Manage_Spawning()
-    aiplane_AssignPlanes()
-    Manage_DebugMode()
-    Manage_SmallMapMode()
-    Projectiles_Manage()
-    Manage_Enemies()
-    plane_RunPropellers()
-
-end
-
-function update()
-    Update_PLANES()
-end
-
-function draw()
-
-    UiColor(1,1,1, 1)
-    UiTextShadow(0,0,0, 1, 0.3, 0)
-    UiFont("bold.ttf", 24)
-
-    Draw_PLANES()
-
-    if Config.draw_projectiles then
-        Projectiles_Draw(200, 500)
-    end
-
-end
-
-
-
+#version 2
 function Manage_Spawning()
 
     local planeVehicles = FindVehicles('planeVehicle', true)
@@ -160,3 +36,74 @@
     end
 end
 
+function server.init()
+    Init_Utils()
+    Init_PLANES()
+    Init_AIPLANES()
+    Init_Config()
+    Init_Sounds()
+    Init_Projectiles()
+    Init_Enemies()
+    Init_Draw()
+    Manage_SmallMapMode()
+    SelectedCamera = CameraPositions[1]
+    SetString("hud.notification", "Note: The F-15 landing gear system is still in development.", true)
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        Tick_Utils()
+        AllVehicles = FindVehicles("", true)
+        FlightMode = GetString("savegame.mod.FlightMode")
+        FlightModeSet = GetBool("savegame.mod.flightmodeset")
+        if not FlightModeSet then
+            SetString("savegame.mod.FlightMode", FlightModes.simple, true)
+            SetBool("savegame.mod.flightmodeset", true, true)
+            print("backup flightmode simple")
+        end
+        dbw("PlayerInPlane", PlayerInPlane)
+        -- Root of plane management.
+        Tick_PLANES()
+        Tick_aiplanes()
+        Manage_Spawning()
+        aiplane_AssignPlanes()
+        Manage_DebugMode()
+        Manage_SmallMapMode()
+        Projectiles_Manage()
+        Manage_Enemies()
+        plane_RunPropellers()
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        Update_PLANES()
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if PlayerInPlane and InputPressed(Config.toggleOptions) then
+
+        ShouldDrawIngameOptions = not ShouldDrawIngameOptions
+        SetBool("level.showedOptions", true, true)
+
+    elseif not PlayerInPlane then
+
+        ShouldDrawIngameOptions = false
+
+    end
+end
+
+function client.draw()
+    UiColor(1,1,1, 1)
+    UiTextShadow(0,0,0, 1, 0.3, 0)
+    UiFont("bold.ttf", 24)
+
+    Draw_PLANES()
+
+    if Config.draw_projectiles then
+        Projectiles_Draw(200, 500)
+    end
+end
+

```

---

# Migration Report: tdapi.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/tdapi.lua
+++ patched/tdapi.lua
@@ -1,4417 +1,1038 @@
+#version 2
+nction GetIntParam(name, default) end
+
+tion GetFloatParam(name, default) end
+
+--
+
+on GetBoolParam(name, default) end
+
+---N
+
+ GetStringParam(name, default) end
+
+---No 
+
+etVersion() end
+
+---No De
+
+Version(version) end
+
+---Returns
+
+me() end
+
+---Returns t
+
+Step() end
+
+---No Descript
+
+PressedKey() end
+
+---No Descriptio
+
+d(input) end
+
 ---No Description
---- 
---- ---
---- Example
----```lua
------Retrieve blinkcount parameter, or set to 5 if omitted
----parameterBlinkCount = GetIntParam("blinkcount", 5)
----```
----@param name string Parameter name
----@param default number Default parameter value
----@return number value Parameter value
-function GetIntParam(name, default) end
+
+(input) end
 
 ---No Description
---- 
---- ---
---- Example
----```lua
------Retrieve speed parameter, or set to 10.0 if omitted
----parameterSpeed = GetFloatParam("speed", 10.0)
----```
----@param name string Parameter name
----@param default number Default parameter value
----@return number value Parameter value
-function GetFloatParam(name, default) end
+--
+
+) end
 
 ---No Description
 --- 
---- ---
---- Example
----```lua
------Retrieve playsound parameter, or false if omitted
----parameterPlaySound = GetBoolParam("playsound", false)
----```
----@param name string Parameter name
----@param default boolean Default parameter value
----@return boolean value Parameter value
-function GetBoolParam(name, default) end
+
+ end
+
+---Set value of a number
+
+lue, transition, time) end
+
+---Calling this function wil
+
+end
+
+---Start a level
+--- 
+--- ---
+
+ layers, passThrough) end
+
+---Set paused state of the game
+
+estart level
+--- 
+--- ---
+--- 
+
+menu
+--- 
+--- ---
+--- 
+
+node, including all
+
+ild keys of a registry nod
+
+ue if the registry contains a
+
+- 
+--- ---
+--- Example
+-
+
+on
+--- 
+--- ---
+--- Example
+---
+
+-- ---
+--- Example
+---``
+
+--- 
+--- ---
+--- Example
+---```l
+
+ ---
+--- Example
+---```lua
+
+--- ---
+--- Example
+---```lua
+-
+
+--- Example
+---```lua
+---
+
+-- ---
+--- Example
+---```lua
+---lo
+
+ly initializes it to the pr
+
+ike regular numbers. Sinc
+
+ple
+---```lua
+---local v 
+
+h, the function returns {0,
+
+mple
+---```lua
+---local v = Ve
+
+ample
+---```lua
+---local a = Vec(
+
+``lua
+---local a = Vec(1,
+
+lua
+---local a = Vec(1,2,
+
+a
+---local a = Vec(1,0,0)
+
+a
+---local a = Vec(2,0,0)
+-
+
+ it to the provided values.
+-
+
+numbers. Since they are
+---im
+
+ecific axis
+--- 
+--- ---
+-
+
+. The order of applied rotations uses t
+
+tions uses the "NASA standard a
+
+d) towards
+---a specific point,
+
+g t. This is
+---very useful for anim
+
+matically
+---equivalent to c = 
+
+```lua
+---local q = QuatEuler(0, 
+
+rot,
+---a vector and quaternion re
+
+hey are
+---implemented with lua 
+
+e opposite of TransformToLocalT
+
+ another transform.
+---This is the opposite of Transfo
+
+ing rotation.
+--- 
+--- ---
+--- Example
+---```lua
+---l
+
+--- ---
+--- Example
+---```lua
+---local
+
+``lua
+---local t = GetBodyTransform(bo
+
+`lua
+---local t = GetBodyTransform(body)
+
+g to an entity
+---SetTag(handle, "specia
+
+--- ---
+--- Example
+---```lua
+---Remove
+
+--local hasSpecial = HasTag(handle,
+
+ue = GetTagValue(handle, "specia
+
+ be provided through the editor. This
+
+apes will show up on the HUD when l
+
+also be removed.
+--- 
+--- ---
+--- Example
+---```
+
+ true if body still exists
+
+ ---
+--- Example
+---```lua
+---loca
+
+ipt scope
+---local target = FindBo
+
+t scope
+---local targets = FindBod
+
+param handle number Body handle
+---@
+
+tBodyTransform(body)
+---t.pos = VecAd
+
+`
+---@param handle number Body handle
+---@return
+
+tion.
+--- 
+--- ---
+--- Example
+-
+
+should leave it up to the engine t
+
+ are better off with a motorized joint inste
+
+-@param handle number Body handle (should be a
+
+-```lua
+---local vel = GetBodyVeloci
+
+ better off with a motorized joint instead.
+--
+
+```
+---@param handle number Body handle (should be 
+
+ of the simulation. This function
+---can be
+
+ine normally handles this automat
+
+(0,1,0)
+---local imp = Vec(0,0,10)
+---Appl
+
+dyShapes(body)
+---for i=1,#shapes do
+---	local shape = s
+
+dle
+---@return number handle Get p
+
+(body)
+---local boundsSize = VecS
+
+)
+---local worldPoint = TransformT
+
+mple
+---```lua
+---if IsBodyVisible(body,
+
+dyBroken(body)
+---```
+---@param handle number Body handle
+---@
+
+d to something static.
+--- 
+--- -
+
+xample
+---```lua
+-----Draw white outline a
+
+--```lua
+---DrawBodyHighlight(body, 0.5)
+---```
+
+t(body, Vec(0, 5, 0))
+---if hit then
+---	--Poi
+
+oal, while not applying an impulse bigger than
+
+---will try to reach the desired goal, while not applying an angular impul
+
+nother body while not affecting the bodies more than the provided 
+---maximum
+
+city to constrain the orientation of one body to the orientation
+---on another b
+
+icitly assigned a body in the editor.
+--- 
+--- ---
+--- Example
+---```lua
+---local w = G
+
+a shape tagged "laserturret
+
+=1, #shapes do
+---	local shape = sh
+
+ody transform in world space
+---loca
+
+nsform)
+---```
+---@param handle number Shap
+
+orldTransform(shape)
+---
+-----This is equivalent to
+--
+
+- Example
+---```lua
+---local body = GetShap
+
+ram shape number Shape handle
+---
+
+ram shape number Shape handle
+---@
+
+x, min)
+---local center = VecLerp(
+
+ emissiveness and light intensity f
+
+en
+---	local hitPoint = VecAdd(pos, VecScale(dir,
+
+related things)
+--- 
+--- ---
+--- Example
+---```lua
+-
+
+eturn number xsize Size in voxels along x axis
+---@re
+
+ape handle
+---@return number coun
+
+n
+---	--Shape is within 25 meters visib
+
+f all voxels are intact.
+--- 
+--- ---
+--- Example
+---```lua
+---
+
+rency
+---DrawShapeOutline(shape, 0
+
+-@param amount number Amount
+function DrawShapeHi
+
+ be in
+---the mask of the other object and vice
+
+Point p of shape s is closest to (0,5,0)
+---end
+---```
+--
+
+---end
+---```
+---@param a number Handle to first
+
+Handle to first location with spec
+
+locations[i]
+---	...
+---end
+---```
+---
+
+n GetLocationTransform(handle) end
+
+---
+
+dle Handle to first joint with specified 
+
+---	...
+---end
+---```
+---@param tag
+
+joint) end
+
+---Joint type is one of 
+
+---	--Joint is rope
+---end
+---``
+
+ointOtherShape(joint, a)
+-----ot
+
+ng this function will override and
+---void an
+
+ angle in degrees (-180 to 180) and velocity
+---is gi
+
+`
+---@param joint number Joint handle
+---@return number min Minim
+
+turn number movement Current joint
+
+param body number Body handle (must 
+
+handle
+function DetachJointFromShap
+
+ight with specified tag or zero if not found
+fu
+
+ string Tag name
+---@param global b
+
+dle number Light handle
+---@param en
+
+or to yellow
+---SetLightColor(light, 1, 1, 0)
+
+le
+---```lua
+-----Pulsate light
+---SetLight
+
+ transform World space light transform
+function G
+
+ end
 
 ---No Description
 --- 
 --- ---
---- Example
----```lua
------Retrieve mode parameter, or "idle" if omitted
----parameterMode = GetSrtingParam("mode", "idle")
----```
----@param name string Parameter name
----@param default string Default parameter value
----@return string value Parameter value
-function GetStringParam(name, default) end
+-
+
+ive(handle) end
 
 ---No Description
---- 
---- ---
---- Example
----```lua
----local v = GetVersion()
------v is "0.5.0"
----```
----@return string version Dot separated string of current version of the game
-function GetVersion() end
+
+n boolean affected Return true if 
+
+ecified tag or zero if not found
+function FindTrig
+
+Tag name
+---@param global boolean Sea
+
+end
 
 ---No Description
 --- 
 --- ---
---- Example
----```lua
----if HasVersion("0.6.0") then
----	--conditional code that only works on 0.6.0 or above
----else
----	--legacy code that works on earlier versions
----end
----```
----@param version string Reference version
----@return boolean match True if current version is at least provided one
-function HasVersion(version) end
-
----Returns running time of this script. If called from update, this returns
----the simulated time, otherwise it returns wall time.
---- 
---- ---
---- Example
----```lua
----local t = GetTime()
----```
----@return number time The time in seconds since level was started
-function GetTime() end
-
----Returns timestep of the last frame. If called from update, this returns
----the simulation time step, which is always one 60th of a second (0.0166667).
----If called from tick or draw it returns the actual time since last frame.
---- 
---- ---
---- Example
----```lua
----local dt = GetTimeStep()
----```
----@return number dt The timestep in seconds
-function GetTimeStep() end
+--
+
+ world space
+function SetTriggerTransfor
+
+umber Trigger handle
+---@return table min Lower poi
+
+ inside True if body is in trigger vo
+
+lean inside True if vehicle is in trigger v
+
+eturn boolean inside True if shape is in trigger 
+
+nside True if point is in trigger volume
+func
+
+t empty then
+---	--highPoint[2] is the talles
+
+ram point table Word space point as vector
+---@
+
+rigger, p)
+---```
+---@param trigger number Trig
+
+ot found
+function FindScreen(tag, global) end
+
+---N
+
+rch in entire scene
+---@return table
+
+--- ---
+--- Example
+---```lua
+---loc
+
+f a screen
+--- 
+--- ---
+--- Example
+---```lua
+
+--- 
+--- ---
+--- Example
+---```lua
+
+dVehicle(tag, global) end
+
+---No De
+
+scene
+---@return table list Indexed t
+
+``lua
+---local body = GetVehicleBody(v
+
+e) end
 
 ---No Description
 --- 
 --- ---
---- Example
----```lua
----name = InputLastPressedKey()
----```
----@return string name Name of last pressed key, empty if no key is pressed
-function InputLastPressedKey() end
+--
+
+`lua
+---local driverPos = GetVehicle
+
+as vector in vehicle space
+function Ge
+
+rwards
+---	local v = FindVehicle("mycar")
+
+le position Player center position
+function GetPlayerPos(playerId) end
+
+f the eye, use GetPlayerCam
+
+))
+---SetPlayerTransform(playerId, t)
+---```
+---@param 
+
+mera transform is usually the same as what you get from 
+
+tPlayerCameraTransform()
+---```
+---@retur
+
+rm) end
 
 ---No Description
 --- 
 --- ---
---- Example
----```lua
----if InputPressed("interact") then
+
+)
+---SetPlayerVehicle(playerId, car)
+---```
+---@param veh
+
+Vec(0, 5, 0))
+---```
+---@param v
+
+e ~= 0 then
 ---	...
 ---end
 ---```
----@param input string The input identifier
----@return boolean pressed True if input was pressed during last frame
-function InputPressed(input) end
+---@
+
+ shape = GetPlayerGrabShape(playerId)
+---if shap
+
+layerGrabBody()
+---if body ~= 0
+
+`lua
+---ReleasePlayerGrab()
+---``
+
+ked shape or zero if nothing is 
+
+yerPickBody()
+---if body ~= 0 th
+
+ which interactable shape is curr
+
+GetPlayerInteractShape(playerId) end
+
+--
+
+tPlayerInteractBody() end
+
+---Set the
+
+--@param handle number Handle to scr
+
+er Set player health (between zero a
+
+on GetPlayerHealth(playerId) end
+
+---R
+
+-Register a custom tool that will sh
+
+istry before it can be used.
+-
+
+l("game.tool.lasergun.enable
+
+olBody~=0 then
+---	...
+---end
+---```
+---@return 
+
+to the right
+---local offs
+
+Distance) end
 
 ---No Description
 --- 
 --- ---
---- Example
----```lua
----if InputReleased("interact") then
----	...
----end
----```
----@param input string The input identifier
----@return boolean pressed True if input was released during last frame
-function InputReleased(input) end
+
+ance) end
 
 ---No Description
 --- 
 --- ---
---- Example
----```lua
----if InputDown("interact") then
----...
----end
----```
----@param input string The input identifier
----@return boolean pressed True if input is currently held down
-function InputDown(input) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----scrollPos = scrollPos + InputValue("mousewheel")
----```
----@param input string The input identifier
----@return number value Depends on input type
-function InputValue(input) end
-
----Set value of a number variable in the global context with an optional transition.
----If a transition is provided the value will animate from current value to the new value during the transition time.
----Transition can be one of the following:
----
----Transition  Description
----linear	 Linear transitioncosine	 Slow at beginning and endeasein	 Slow at beginningeaseout	 Slow at endbounce	 Bounce and overshoot new value
---- 
---- ---
---- Example
----```lua
----myValue = 0
----SetValue("myValue", 1, "linear", 0.5)
----
----This will change the value of myValue from 0 to 1 in a linear fasion over 0.5 seconds
----```
----@param variable string Name of number variable in the global context
----@param value number The new value
----@param transition string Transition type. See description.
----@param time number Transition time (seconds)
-function SetValue(variable, value, transition, time) end
-
----Calling this function will add a button on the bottom bar when the game is paused. Use this
----as a way to bring up mod settings or other user interfaces while the game is running. 
----Call this function every frame from the tick function for as long as the pause menu button
----should still be visible.
---- 
---- ---
---- Example
----```lua
----function tick()
----	if PauseMenuButton("MyMod Settings") then
----		visible = true
----	end
----end
----
----function draw()
----	if visible then
----		UiMakeInteractive()
----		...
----	end
----end
----```
----@param title string Text on button
----@return boolean clicked True if clicked, false otherwise
-function PauseMenuButton(title) end
-
----Start a level
---- 
---- ---
---- Example
----```lua
------Start level with no active layers
----StartLevel("level1", "MOD/level1.xml")
----
------Start level with two layers
----StartLevel("level1", "MOD/level1.xml", "vehicles targets")
----```
----@param mission string An identifier of your choice
----@param path string Path to level XML file
----@param layers string Active layers. Default is no layers.
----@param passThrough boolean If set, loading screen will have no text and music will keep playing
-function StartLevel(mission, path, layers, passThrough) end
-
----Set paused state of the game
---- 
---- ---
---- Example
----```lua
------Pause game and bring up pause menu on HUD
----SetPaused(true)
----```
----@param paused boolean True if game should be paused
-function SetPaused(paused) end
-
----Restart level
---- 
---- ---
---- Example
----```lua
----if shouldRestart then
----Restart()
----end
----```
-function Restart() end
-
----Go to main menu
---- 
---- ---
---- Example
----```lua
----if shouldExitLevel then
----Menu()
----end
----```
-function Menu() end
-
----Remove registry node, including all child nodes.
---- 
---- ---
---- Example
----```lua
------If the registry looks like this:
------	score
------		levels
------			level1 = 5
------			level2 = 4
----
----ClearKey("score.levels")
----
------Afterwards, the registry will look like this:
------	score
----```
----@param key string Registry key to clear
-function ClearKey(key) end
-
----List all child keys of a registry node.
---- 
---- ---
---- Example
----```lua
------If the registry looks like this:
------	score
------		levels
------			level1 = 5
------			level2 = 4
----
----local list = ListKeys("score.levels")
----for i=1, #list do
----	print(list[i])
----end
----
------This will output:
------level1
------level2
----```
----@param parent string The parent registry key
----@return table children Indexed table of strings with child keys
-function ListKeys(parent) end
-
----Returns true if the registry contains a certain key
---- 
---- ---
---- Example
----```lua
----local foo = HasKey("score.levels")
----```
----@param key string Registry key
----@return boolean exists True if key exists
-function HasKey(key) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----SetInt("score.levels.level1", 4)
----```
----@param key string Registry key
----@param value number Desired value
-function SetInt(key, value) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local a = GetInt("score.levels.level1")
----```
----@param key string Registry key
----@return number value Integer value of registry node or zero if not found
-function GetInt(key) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----SetFloat("level.time", 22.3)
----```
----@param key string Registry key
----@param value number Desired value
-function SetFloat(key, value) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local time = GetFloat("level.time")
----```
----@param key string Registry key
----@return number value Float value of registry node or zero if not found
-function GetFloat(key) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----SetBool("level.robots.enabled", true)
----```
----@param key string Registry key
----@param value boolean Desired value
-function SetBool(key, value) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local isRobotsEnabled = GetBool("level.robots.enabled")
----```
----@param key string Registry key
----@return boolean value Boolean value of registry node or false if not found
-function GetBool(key) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----SetString("level.name", "foo")
----```
----@param key string Registry key
----@param value string Desired value
-function SetString(key, value) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local name = GetString("level.name")
----```
----@param key string Registry key
----@return string value String value of registry node or "" if not found
-function GetString(key) end
-
----Create new vector and optionally initializes it to the provided values.
----A Vec is equivalent to a regular lua table with three numbers.
---- 
---- ---
---- Example
----```lua
------These are equivalent
----local a1 = Vec()
----local a2 = {0, 0, 0}
----
------These are equivalent
----local b1 = Vec(0, 1, 0)
----local b2 = {0, 1, 0}
----```
----@param x number X value
----@param y number Y value
----@param z number Z value
----@return table vec New vector
-function Vec(x, y, z) end
-
----Vectors should never be assigned like regular numbers. Since they are
----implemented with lua tables assignment means two references pointing to
----the same data. Use this function instead.
---- 
---- ---
---- Example
----```lua
------Do this to assign a vector
----local right1 = Vec(1, 2, 3)
----local right2 = VecCopy(right1)
----
------Never do this unless you REALLY know what you're doing
----local wrong1 = Vec(1, 2, 3)
----local wrong2 = wrong1
----```
----@param org table A vector
----@return table new Copy of org vector
-function VecCopy(org) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local v = Vec(1,1,0)
----local l = VecLength(v)
----
------l now equals 1.41421356
----```
----@param vec table A vector
----@return number length Length (magnitude) of the vector
-function VecLength(vec) end
-
----If the input vector is of zero length, the function returns {0,0,1}
---- 
---- ---
---- Example
----```lua
----local v = Vec(0,3,0)
----local n = VecNormalize(v)
----
------n now equals {0,1,0}
----```
----@param vec table A vector
----@return table norm A vector of length 1.0
-function VecNormalize(vec) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local v = Vec(1,2,3)
----local n = VecScale(v, 2)
----
------n now equals {2,4,6}
----```
----@param vec table A vector
----@param scale number A scale factor
----@return table norm A scaled version of input vector
-function VecScale(vec, scale) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local a = Vec(1,2,3)
----local b = Vec(3,0,0)
----local c = VecAdd(a, b)
----
------c now equals {4,2,3}
----```
----@param a table Vector
----@param b table Vector
----@return table c New vector with sum of a and b
-function VecAdd(a, b) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local a = Vec(1,2,3)
----local b = Vec(3,0,0)
----local c = VecSub(a, b)
----
------c now equals {-2,2,3}
----```
----@param a table Vector
----@param b table Vector
----@return table c New vector representing a-b
-function VecSub(a, b) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local a = Vec(1,2,3)
----local b = Vec(3,1,0)
----local c = VecDot(a, b)
----
------c now equals 5
----```
----@param a table Vector
----@param b table Vector
----@return number c Dot product of a and b
-function VecDot(a, b) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local a = Vec(1,0,0)
----local b = Vec(0,1,0)
----local c = VecCross(a, b)
----
------c now equals {0,0,1}
----```
----@param a table Vector
----@param b table Vector
----@return table c Cross product of a and b (also called vector product)
-function VecCross(a, b) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local a = Vec(2,0,0)
----local b = Vec(0,4,2)
----local t = 0.5
----
------These two are equivalent
----local c1 = VecLerp(a, b, t)
----lcoal c2 = VecAdd(VecScale(a, 1-t), VecScale(b, t))
----
------c1 and c2 now equals {1, 2, 1}
----```
----@param a table Vector
----@param b table Vector
----@param t number fraction (usually between 0.0 and 1.0)
----@return table c Linearly interpolated vector between a and b, using t
-function VecLerp(a, b, t) end
-
----Create new quaternion and optionally initializes it to the provided values.
----Do not attempt to initialize a quaternion with raw values unless you know
----what you are doing. Use QuatEuler or QuatAxisAngle instead.
----If no arguments are given, a unit quaternion will be created: {0, 0, 0, 1}.
----A quaternion is equivalent to a regular lua table with four numbers.
---- 
---- ---
---- Example
----```lua
------These are equivalent
----local a1 = Quat()
----local a2 = {0, 0, 0, 1}
----```
----@param x number X value
----@param y number Y value
----@param z number Z value
----@param w number W value
----@return table quat New quaternion
-function Quat(x, y, z, w) end
-
----Quaternions should never be assigned like regular numbers. Since they are
----implemented with lua tables assignment means two references pointing to
----the same data. Use this function instead.
---- 
---- ---
---- Example
----```lua
------Do this to assign a quaternion
----local right1 = QuatEuler(0, 90, 0)
----local right2 = QuatCopy(right1)
----
------Never do this unless you REALLY know what you're doing
----local wrong1 = QuatEuler(0, 90, 0)
----local wrong2 = wrong1
----```
----@param org table Quaternion
----@return table new Copy of org quaternion
-function QuatCopy(org) end
-
----Create a quaternion representing a rotation around a specific axis
---- 
---- ---
---- Example
----```lua
------Create quaternion representing rotation 30 degrees around Y axis
----local q = QuatAxisAngle(Vec(0,1,0), 30)
----```
----@param axis table Rotation axis, unit vector
----@param angle number Rotation angle in degrees
----@return table quat New quaternion
-function QuatAxisAngle(axis, angle) end
-
----Create quaternion using euler angle notation. The order of applied rotations uses the
----"NASA standard aeroplane" model:
----Rotation around Y axis (yaw or heading)
----Rotation around Z axis (pitch or attitude)
----Rotation around X axis (roll or bank)
---- 
---- ---
---- Example
----```lua
------Create quaternion representing rotation 30 degrees around Y axis and 25 degrees around Z axis
----local q = QuatEuler(0, 30, 25)
----```
----@param x number Angle around X axis in degrees, sometimes also called roll or bank
----@param y number Angle around Y axis in degrees, sometimes also called yaw or heading
----@param z number Angle around Z axis in degrees, sometimes also called pitch or attitude
----@return table quat New quaternion
-function QuatEuler(x, y, z) end
-
----Return euler angles from quaternion. The order of rotations uses the "NASA standard aeroplane" model:
----Rotation around Y axis (yaw or heading)
----Rotation around Z axis (pitch or attitude)
----Rotation around X axis (roll or bank)
---- 
---- ---
---- Example
----```lua
------Return euler angles from quaternion q
----rx, ry, rz = GetQuatEuler(q)
----```
----@param quat table Quaternion
----@return number x Angle around X axis in degrees, sometimes also called roll or bank
----@return number y Angle around Y axis in degrees, sometimes also called yaw or heading
----@return number z Angle around Z axis in degrees, sometimes also called pitch or attitude
-function GetQuatEuler(quat) end
-
----Create a quaternion pointing the negative Z axis (forward) towards
----a specific point, keeping the Y axis upwards. This is very useful
----for creating camera transforms.
---- 
---- ---
---- Example
----```lua
----local eye = Vec(0, 10, 0)
----local target = Vec(0, 1, 5)
----local rot = QuatLookAt(eye, target)
----SetCameraTransform(Transform(eye, rot))
----```
----@param eye table Vector representing the camera location
----@param target table Vector representing the point to look at
----@return table quat New quaternion
-function QuatLookAt(eye, target) end
-
----Spherical, linear interpolation between a and b, using t. This is
----very useful for animating between two rotations.
---- 
---- ---
---- Example
----```lua
----local a = QuatEuler(0, 10, 0)
----local b = QuatEuler(0, 0, 45)
----
------Create quaternion half way between a and b
----local q = QuatSlerp(a, b, 0.5)
----```
----@param a table Quaternion
----@param b table Quaternion
----@param t number fraction (usually between 0.0 and 1.0)
----@return table c New quaternion
-function QuatSlerp(a, b, t) end
-
----Rotate one quaternion with another quaternion. This is mathematically
----equivalent to c = a * b using quaternion multiplication.
---- 
---- ---
---- Example
----```lua
----local a = QuatEuler(0, 10, 0)
----local b = QuatEuler(0, 0, 45)
----local q = QuatRotateQuat(a, b)
----
------q now represents a rotation first 10 degrees around
------the Y axis and then 45 degrees around the Z axis.
----```
----@param a table Quaternion
----@param b table Quaternion
----@return table c New quaternion
-function QuatRotateQuat(a, b) end
-
----Rotate a vector by a quaternion
---- 
---- ---
---- Example
----```lua
----local q = QuatEuler(0, 10, 0)
----local v = Vec(1, 0, 0)
----local r = QuatRotateVec(q, v)
----
------r is now vector a rotated 10 degrees around the Y axis
----```
----@param a table Quaternion
----@param vec table Vector
----@return table vec Rotated vector
-function QuatRotateVec(a, vec) end
-
----A transform is a regular lua table with two entries: pos and rot,
----a vector and quaternion representing transform position and rotation.
---- 
---- ---
---- Example
----```lua
------Create transform located at {0, 0, 0} with no rotation
----local t1 = Transform()
----
------Create transform located at {10, 0, 0} with no rotation
----local t2 = Transform(Vec(10, 0,0))
----
------Create transform located at {10, 0, 0}, rotated 45 degrees around Y axis
----local t2 = Transform(Vec(10, 0,0), QuatEuler(0, 45, 0))
----```
----@param pos table Vector representing transform position
----@param rot table Quaternion representing transform rotation
----@return table transform New transform
-function Transform(pos, rot) end
-
----Transforms should never be assigned like regular numbers. Since they are
----implemented with lua tables assignment means two references pointing to
----the same data. Use this function instead.
---- 
---- ---
---- Example
----```lua
------Do this to assign a quaternion
----local right1 = Transform(Vec(1,0,0), QuatEuler(0, 90, 0))
----local right2 = TransformCopy(right1)
----
------Never do this unless you REALLY know what you're doing
----local wrong1 = Transform(Vec(1,0,0), QuatEuler(0, 90, 0))
----local wrong2 = wrong1
----```
----@param org table Transform
----@return table new Copy of org transform
-function TransformCopy(org) end
-
----Transform child transform out of the parent transform.
----This is the opposite of TransformToLocalTransform.
---- 
---- ---
---- Example
----```lua
----local b = GetBodyTransform(body)
----local s = GetShapeLocalTransform(shape)
----
------b represents the location of body in world space
------s represents the location of shape in body space
----
----local w = TransformToParentTransform(b, s)
----
------w now represents the location of shape in world space
----```
----@param parent table Transform
----@param child table Transform
----@return table transform New transform
-function TransformToParentTransform(parent, child) end
-
----Transform one transform into the local space of another transform.
----This is the opposite of TransformToParentTransform.
---- 
---- ---
---- Example
----```lua
----local b = GetBodyTransform(body)
----local w = GetShapeWorldTransform(shape)
----
------b represents the location of body in world space
------w represents the location of shape in world space
----
----local s = TransformToLocalTransform(b, w)
----
------s now represents the location of shape in body space.
----```
----@param parent table Transform
----@param child table Transform
----@return table transform New transform
-function TransformToLocalTransform(parent, child) end
-
----Transfom vector v out of transform t only considering rotation.
---- 
---- ---
---- Example
----```lua
----local t = GetBodyTransform(body)
----local localUp = Vec(0, 1, 0)
----local up = TransformToParentVec(t, localUp)
----
------up now represents the local body up direction in world space
----```
----@param t table Transform
----@param v table Vector
----@return table r Transformed vector
-function TransformToParentVec(t, v) end
-
----Transfom vector v into transform t only considering rotation.
---- 
---- ---
---- Example
----```lua
----local t = GetBodyTransform(body)
----local worldUp = Vec(0, 1, 0)
----local up = TransformToLocalVec(t, worldUp)
----
------up now represents the world up direction in local body space
----```
----@param t table Transform
----@param v table Vector
----@return table r Transformed vector
-function TransformToLocalVec(t, v) end
-
----Transfom position p out of transform t.
---- 
---- ---
---- Example
----```lua
----local t = GetBodyTransform(body)
----local bodyPoint = Vec(0, 0, -1)
----local p = TransformToParentPoint(t, bodyPoint)
----
------p now represents the local body point {0, 0, -1 } in world space
----```
----@param t table Transform
----@param p table Vector representing position
----@return table r Transformed position
-function TransformToParentPoint(t, p) end
-
----Transfom position p into transform t.
---- 
---- ---
---- Example
----```lua
----local t = GetBodyTransform(body)
----local worldOrigo = Vec(0, 0, 0)
----local p = TransformToLocalPoint(t, worldOrigo)
----
------p now represents the position of world origo in local body space
----```
----@param t table Transform
----@param p table Vector representing position
----@return table r Transformed position
-function TransformToLocalPoint(t, p) end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Add "special" tag to an entity
----SetTag(handle, "special")
----
------Add "team" tag to an entity and give it value "red"
----SetTag(handle, "team", "red")
----```
----@param handle number Entity handle
----@param tag string Tag name
----@param value string Tag value
-function SetTag(handle, tag, value) end
-
----Remove tag from an entity. If the tag had a value it is removed too.
---- 
---- ---
---- Example
----```lua
----RemoveTag(handle, "special")
----```
----@param handle number Entity handle
----@param tag string Tag name
-function RemoveTag(handle, tag) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----SetTag(handle, "special")
----local hasSpecial = HasTag(handle, "special") 
------ hasSpecial will be true
----```
----@param handle number Entity handle
----@param tag string Tag name
----@return boolean exists Returns true if entity has tag
-function HasTag(handle, tag) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----SetTag(handle, "special")
----value = GetTagValue(handle, "special")
------ value will be ""
----
----SetTag(handle, "special", "foo")
----value = GetTagValue(handle, "special")
------ value will be "foo"
----```
----@param handle number Entity handle
----@param tag string Tag name
----@return string value Returns the tag value, if any. Empty string otherwise.
-function GetTagValue(handle, tag) end
-
----All entities can have an associated description. For bodies and
----shapes this can be provided through the editor. This function 
----retrieves that description.
---- 
---- ---
---- Example
----```lua
----local desc = GetDescription(body)
----```
----@param handle number Entity handle
----@return string description The description string
-function GetDescription(handle) end
-
----All entities can have an associated description. The description for 
----bodies and shapes will show up on the HUD when looking at them.
---- 
---- ---
---- Example
----```lua
----SetDescription(body, "Target object")
----```
----@param handle number Entity handle
----@param description string The description string
-function SetDescription(handle, description) end
-
----Remove an entity from the scene. All entities owned by this entity
----will also be removed.
---- 
---- ---
---- Example
----```lua
----Delete(body)
------All shapes associated with body will also be removed
----```
----@param handle number Entity handle
-function Delete(handle) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----valid = IsHandleValid(body)
----
------valid is true if body still exists
----
----Delete(body)
----valid = IsHandleValid(body)
----
------valid will now be false
----```
----@param handle number Entity handle
----@return boolean exists Returns true if the entity pointed to by handle still exists
-function IsHandleValid(handle) end
-
----Returns the type name of provided entity, for example "body", "shape", "light", etc.
---- 
---- ---
---- Example
----```lua
----local t = GetEntityType(e)
----if t == "body" then
----	--e is a body handle
----end
----```
----@param handle number Entity handle
----@return string type Type name of the provided entity
-function GetEntityType(handle) end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Search for a body tagged "target" in script scope
----local target = FindBody("target")
----
------Search for a body tagged "escape" in entire scene
----local escape = FindBody("escape", true)
----```
----@param tag string Tag name
----@param global boolean Search in entire scene
----@return number handle Handle to first body with specified tag or zero if not found
-function FindBody(tag, global) end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Search for bodies tagged "target" in script scope
----local targets = FindBodies("target")
----for i=1, #targets do
----	local target = targets[i]
----	...
----end
----```
----@param tag string Tag name
----@param global boolean Search in entire scene
----@return table list Indexed table with handles to all bodies with specified tag
-function FindBodies(tag, global) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local t = GetBodyTransform(body)
----```
----@param handle number Body handle
----@return table transform Transform of the body
-function GetBodyTransform(handle) end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Move a body 1 meter upwards
----local t = GetBodyTransform(body)
----t.pos = VecAdd(t.pos, Vec(0, 1, 0))
----SetBodyTransform(body, t)
----```
----@param handle number Body handle
----@param transform table Desired transform
-function SetBodyTransform(handle, transform) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local mass = GetBodyMass(body)
----```
----@param handle number Body handle
----@return number mass Body mass. Static bodies always return zero mass.
-function GetBodyMass(handle) end
-
----Check if body is dynamic. Note that something that was created static 
----may become dynamic due to destruction.
---- 
---- ---
---- Example
----```lua
----local dynamic = IsBodyDynamic(body)
----```
----@param handle number Body handle
----@return boolean dynamic Return true if body is dynamic
-function IsBodyDynamic(handle) end
-
----Change the dynamic state of a body. There is very limited use for this
----function. In most situations you should leave it up to the engine to decide.
----Use with caution.
---- 
---- ---
---- Example
----```lua
----SetBodyDynamic(body, false)
----```
----@param handle number Body handle
----@param dynamic boolean True for dynamic. False for static.
-function SetBodyDynamic(handle, dynamic) end
-
----This can be used for animating bodies with preserved physical interaction,
----but in most cases you are better off with a motorized joint instead.
---- 
---- ---
---- Example
----```lua
----local vel = Vec(2,0,0)
----SetBodyVelocity(body, vel)
----```
----@param handle number Body handle (should be a dynamic body)
----@param velocity table Vector with linear velocity
-function SetBodyVelocity(handle, velocity) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local linVel = GetBodyVelocity(body)
----```
----@param handle number Body handle (should be a dynamic body)
----@return table velocity Linear velocity as vector
-function GetBodyVelocity(handle) end
-
----Return the velocity on a body taking both linear and angular velocity into account.
---- 
---- ---
---- Example
----```lua
----local vel = GetBodyVelocityAtPos(body, pos)
----```
----@param handle number Body handle (should be a dynamic body)
----@param pos table World space point as vector
----@return table velocity Linear velocity on body at pos as vector
-function GetBodyVelocityAtPos(handle, pos) end
-
----This can be used for animating bodies with preserved physical interaction,
----but in most cases you are better off with a motorized joint instead.
---- 
---- ---
---- Example
----```lua
----local angVel = Vec(2,0,0)
----SetBodyAngularVelocity(body, angVel)
----```
----@param handle number Body handle (should be a dynamic body)
----@param angVel table Vector with angular velocity
-function SetBodyAngularVelocity(handle, angVel) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local angVel = GetBodyAngularVelocity(body)
----```
----@param handle number Body handle (should be a dynamic body)
----@return table angVel Angular velocity as vector
-function GetBodyAngularVelocity(handle) end
-
----Check if body is body is currently simulated. For performance reasons,
----bodies that don't move are taken out of the simulation. This function
----can be used to query the active state of a specific body. Only dynamic
----bodies can be active.
---- 
---- ---
---- Example
----```lua
----if IsBodyActive(body) then
----	...
----end
----```
----@param handle number Body handle
----@return boolean active Return true if body is active
-function IsBodyActive(handle) end
-
----This function makes it possible to manually activate and deactivate bodies to include or
----exclude in simulation. The engine normally handles this automatically, so use with care.
---- 
---- ---
---- Example
----```lua
------Wake up body
----SetBodyActive(body, true)
----
------Put body to sleep
----SetBodyActive(body, false)
----```
----@param handle number Body handle
----@param active boolean Set to tru if body should be active (simulated)
-function SetBodyActive(handle, active) end
-
----Apply impulse to dynamic body at position (give body a push).
---- 
---- ---
---- Example
----```lua
----local pos = Vec(0,1,0)
----local imp = Vec(0,0,10)
----ApplyBodyImpulse(body, pos, imp)
----```
----@param handle number Body handle (should be a dynamic body)
----@param position table World space position as vector
----@param impulse table World space impulse as vector
-function ApplyBodyImpulse(handle, position, impulse) end
-
----Return handles to all shapes owned by a body
---- 
---- ---
---- Example
----```lua
----local shapes = GetBodyShapes(body)
----for i=1,#shapes do
----	local shape = shapes[i]
----end
----```
----@param handle number Body handle
----@return table list Indexed table of shape handles
-function GetBodyShapes(handle) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local vehicle = GetBodyVehicle(body)
----```
----@param body number Body handle
----@return number handle Get parent vehicle for body, or zero if not part of vehicle
-function GetBodyVehicle(body) end
-
----Return the world space, axis-aligned bounding box for a body.
---- 
---- ---
---- Example
----```lua
----local min, max = GetBodyBounds(body)
----local boundsSize = VecSub(max, min)
----local center = VecLerp(min, max, 0.5)
----```
----@param handle number Body handle
----@return table min Vector representing the AABB lower bound
----@return table max Vector representing the AABB upper bound
-function GetBodyBounds(handle) end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Visualize center of mass on for body
----local com = GetBodyCenterOfMass(body)
----local worldPoint = TransformToParentPoint(GetBodyTransform(body), com)
----DebugCross(worldPoint)
----```
----@param handle number Body handle
----@return table point Vector representing local center of mass in body space
-function GetBodyCenterOfMass(handle) end
-
----This will check if a body is currently visible in the camera frustum and
----not occluded by other objects.
---- 
---- ---
---- Example
----```lua
----if IsBodyVisible(body, 25) then
----	--Body is within 25 meters visible to the camera
----end
----```
----@param handle number Body handle
----@param maxDist number Maximum visible distance
----@param rejectTransparent boolean See through transparent materials. Default false.
----@return boolean visible Return true if body is visible
-function IsBodyVisible(handle, maxDist, rejectTransparent) end
-
----Determine if any shape of a body has been broken.
---- 
---- ---
---- Example
----```lua
----local broken = IsBodyBroken(body)
----```
----@param handle number Body handle
----@return boolean broken Return true if body is broken
-function IsBodyBroken(handle) end
-
----Determine if a body is in any way connected to a static object, either by being static itself or
----be being directly or indirectly jointed to something static.
---- 
---- ---
---- Example
----```lua
----local connectedToStatic = IsBodyJointedToStatic(body)
----```
----@param handle number Body handle
----@return boolean result Return true if body is in any way connected to a static body
-function IsBodyJointedToStatic(handle) end
-
----Render next frame with an outline around specified body.
----If no color is given, a white outline will be drawn.
---- 
---- ---
---- Example
----```lua
------Draw white outline at 50% transparency
----DrawBodyOutline(body, 0.5)
----
------Draw green outline, fully opaque
----DrawBodyOutline(body, 0, 1, 0, 1)
----```
----@param handle number Body handle
----@param r number Red
----@param g number Green
----@param b number Blue
----@param a number Alpha
-function DrawBodyOutline(handle, r, g, b, a) end
-
----Flash the appearance of a body when rendering this frame. This is
----used for valuables in the game.
---- 
---- ---
---- Example
----```lua
----DrawBodyHighlight(body, 0.5)
----```
----@param handle number Body handle
----@param amount number Amount
-function DrawBodyHighlight(handle, amount) end
-
----This will return the closest point of a specific body
---- 
---- ---
---- Example
----```lua
----local hit, p, n, s = GetBodyClosestPoint(body, Vec(0, 5, 0))
----if hit then
----	--Point p of shape s is closest
----end
----```
----@param body number Body handle
----@param origin table World space point
----@return boolean hit True if a point was found
----@return table point World space closest point
----@return table normal World space normal at closest point
----@return number shape Handle to closest shape
-function GetBodyClosestPoint(body, origin) end
-
----This will tell the physics solver to constrain the velocity between two bodies. The physics solver
----will try to reach the desired goal, while not applying an impulse bigger than the min and max values.
----This function should only be used from the update callback.
---- 
---- ---
---- Example
----```lua
------Constrain the velocity between bodies A and B so that the relative velocity 
------along the X axis at point (0, 5, 0) is always 3 m/s
----ConstrainVelocity(a, b, Vec(0, 5, 0), Vec(1, 0, 0), 3)
----```
----@param bodyA number First body handle (zero for static)
----@param bodyB number Second body handle (zero for static)
----@param point table World space point
----@param dir table World space direction
----@param relVel number Desired relative velocity along the provided direction
----@param min number Minimum impulse (default: -infinity)
----@param max number Maximum impulse (default: infinity)
-function ConstrainVelocity(bodyA, bodyB, point, dir, relVel, min, max) end
-
----This will tell the physics solver to constrain the angular velocity between two bodies. The physics solver
----will try to reach the desired goal, while not applying an angular impulse bigger than the min and max values.
----This function should only be used from the update callback.
---- 
---- ---
---- Example
----```lua
------Constrain the angular velocity between bodies A and B so that the relative angular velocity
------along the Y axis is always 3 rad/s
----ConstrainAngularVelocity(a, b, Vec(1, 0, 0), 3)
----```
----@param bodyA number First body handle (zero for static)
----@param bodyB number Second body handle (zero for static)
----@param dir table World space direction
----@param relAngVel number Desired relative angular velocity along the provided direction
----@param min number Minimum angular impulse (default: -infinity)
----@param max number Maximum angular impulse (default: infinity)
-function ConstrainAngularVelocity(bodyA, bodyB, dir, relAngVel, min, max) end
-
----This is a helper function that uses ConstrainVelocity to constrain a point on one 
----body to a point on another body while not affecting the bodies more than the provided 
----maximum relative velocity and maximum impulse. In other words: physically push on
----the bodies so that pointA and pointB are aligned in world space. This is useful for 
----physically animating objects. This function should only be used from the update callback.
---- 
---- ---
---- Example
----```lua
------Constrain the origo of body a to an animated point in the world
----local worldPos = Vec(0, 3+math.sin(GetTime()), 0)
----ConstrainPosition(a, 0, GetBodyTransform(a).pos, worldPos)
----
------Constrain the origo of body a to the origo of body b (like a ball joint)
----ConstrainPosition(a, b, GetBodyTransform(a).pos, GetBodyTransform(b).pos)
----```
----@param bodyA number First body handle (zero for static)
----@param bodyB number Second body handle (zero for static)
----@param pointA table World space point for first body
----@param pointB table World space point for second body
----@param maxVel number Maximum relative velocity (default: infinite)
----@param maxImpulse number Maximum impulse (default: infinite)
-function ConstrainPosition(bodyA, bodyB, pointA, pointB, maxVel, maxImpulse) end
-
----This is the angular counterpart to ConstrainPosition, a helper function that uses
----ConstrainAngularVelocity to constrain the orientation of one body to the orientation
----on another body while not affecting the bodies more than the provided maximum relative
----angular velocity and maximum angular impulse. In other words: physically rotate the
----bodies so that quatA and quatB are aligned in world space. This is useful for 
----physically animating objects. This function should only be used from the update callback.
---- 
---- ---
---- Example
----```lua
------Constrain the orietation of body a to an upright orientation in the world
----ConstrainOrientation(a, 0, GetBodyTransform(a).rot, Quat())
----
------Constrain the orientation of body a to the orientation of body b
----ConstrainOrientation(a, b, GetBodyTransform(a).rot, GetBodyTransform(b).rot)
----```
----@param bodyA number First body handle (zero for static)
----@param bodyB number Second body handle (zero for static)
----@param quatA table World space orientation for first body
----@param quatB table World space orientation for second body
----@param maxAngVel number Maximum relative angular velocity (default: infinite)
----@param maxAngImpulse number Maximum angular impulse (default: infinite)
-function ConstrainOrientation(bodyA, bodyB, quatA, quatB, maxAngVel, maxAngImpulse) end
-
----Every scene in Teardown has an implicit static world body that contains all shapes that are not explicitly assigned a body in the editor.
---- 
---- ---
---- Example
----```lua
----local w = GetWorldBody()
----```
----@return number body Handle to the static world body
-function GetWorldBody() end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Search for a shape tagged "mybox" in script scope
----local target = FindShape("mybox")
----
------Search for a shape tagged "laserturret" in entire scene
----local escape = FindShape("laserturret", true)
----```
----@param tag string Tag name
----@param global boolean Search in entire scene
----@return number handle Handle to first shape with specified tag or zero if not found
-function FindShape(tag, global) end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Search for shapes tagged "alarmbox" in script scope
----local shapes = FindShapes("alarmbox")
----for i=1, #shapes do
----	local shape = shapes[i]
----	...
----end
----```
----@param tag string Tag name
----@param global boolean Search in entire scene
----@return table list Indexed table with handles to all shapes with specified tag
-function FindShapes(tag, global) end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Shape transform in body local space
----local shapeTransform = GetShapeLocalTransform(shape)
----
------Body transform in world space
----local bodyTransform = GetBodyTransform(GetShapeBody(shape))
----
------Shape transform in world space
----local worldTranform = TransformToParentTransform(bodyTransform, shapeTransform)
----```
----@param handle number Shape handle
----@return table transform Return shape transform in body space
-function GetShapeLocalTransform(handle) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local transform = Transform(Vec(0, 1, 0), QuatEuler(0, 90, 0))
----SetShapeLocalTransform(shape, transform)
----```
----@param handle number Shape handle
----@param transform table Shape transform in body space
-function SetShapeLocalTransform(handle, transform) end
-
----This is a convenience function, transforming the shape out of body space
---- 
---- ---
---- Example
----```lua
----local worldTransform = GetShapeWorldTransform(shape)
----
------This is equivalent to
----local shapeTransform = GetShapeLocalTransform(shape)
----local bodyTransform = GetBodyTransform(GetShapeBody(shape))
----worldTranform = TransformToParentTransform(bodyTransform, shapeTransform)
----```
----@param handle number Shape handle
----@return table transform Return shape transform in world space
-function GetShapeWorldTransform(handle) end
-
----Get handle to the body this shape is owned by. A shape is always owned by a body,
----but can be transfered to a new body during destruction.
---- 
---- ---
---- Example
----```lua
----local body = GetShapeBody(shape)
----```
----@param handle number Shape handle
----@return number handle Body handle
-function GetShapeBody(handle) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local hinges = GetShapeJoints(door)
----for i=1, #hinges do
----	local joint = hinges[i]
----	...
----end
----```
----@param shape number Shape handle
----@return table list Indexed table with joints connected to shape
-function GetShapeJoints(shape) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local lights = GetShapeLights(shape)
----for i=1, #lights do
----	local light = lights[i]
----	...
----end
----```
----@param shape number Shape handle
----@return table list Indexed table of lights owned by shape
-function GetShapeLights(shape) end
-
----Return the world space, axis-aligned bounding box for a shape.
---- 
---- ---
---- Example
----```lua
----local min, max = GetShapeBounds(shape)
----local boundsSize = VecSub(max, min)
----local center = VecLerp(min, max, 0.5)
----```
----@param handle number Shape handle
----@return table min Vector representing the AABB lower bound
----@return table max Vector representing the AABB upper bound
-function GetShapeBounds(handle) end
-
----Scale emissiveness for shape. If the shape has light sources attached,
----their intensity will be scaled by the same amount.
---- 
---- ---
---- Example
----```lua
------Pulsate emissiveness and light intensity for shape
----local scale = math.sin(GetTime())*0.5 + 0.5
----SetShapeEmissiveScale(shape, scale)
----```
----@param handle number Shape handle
----@param scale number Scale factor for emissiveness
-function SetShapeEmissiveScale(handle, scale) end
-
----Return material properties for a particular voxel
---- 
---- ---
---- Example
----```lua
----local hit, dist, normal, shape = QueryRaycast(pos, dir, 10)
----if hit then
----	local hitPoint = VecAdd(pos, VecScale(dir, dist))
----	local mat = GetShapeMaterialAtPosition(shape, hitPoint)
----	DebugPrint("Raycast hit voxel made out of " .. mat)
----end
----```
----@param handle number Shape handle
----@param pos table Position in world space
----@return string type Material type
----@return number r Red
----@return number g Green
----@return number b Blue
----@return number a Alpha
-function GetShapeMaterialAtPosition(handle, pos) end
-
----Return material properties for a particular voxel in the voxel grid indexed by integer values.
----The first index is zero (not one, as opposed to a lot of lua related things)
---- 
---- ---
---- Example
----```lua
----local mat = GetShapeMaterialAtIndex(shape, 0, 0, 0)
----DebugPrint("The voxel closest to origo is of material: " .. mat)
----```
----@param handle number Shape handle
----@param x number X integer coordinate
----@param y number Y integer coordinate
----@param z number Z integer coordinate
----@return string type Material type
----@return number r Red
----@return number g Green
----@return number b Blue
----@return number a Alpha
-function GetShapeMaterialAtIndex(handle, x, y, z) end
-
----Return the size of a shape in voxels
---- 
---- ---
---- Example
----```lua
----local x, y, z = GetShapeSize(shape)
----```
----@param handle number Shape handle
----@return number xsize Size in voxels along x axis
----@return number ysize Size in voxels along y axis
----@return number zsize Size in voxels along z axis
----@return number scale The size of one voxel in meters (with default scale it is 0.1)
-function GetShapeSize(handle) end
-
----Return the number of voxels in a shape, not including empty space
---- 
---- ---
---- Example
----```lua
----local voxelCount = GetShapeVoxelCount(shape)
----```
----@param handle number Shape handle
----@return number count Number of voxels in shape
-function GetShapeVoxelCount(handle) end
-
----This will check if a shape is currently visible in the camera frustum and
----not occluded by other objects.
---- 
---- ---
---- Example
----```lua
----if IsShapeVisible(shape, 25) then
----	--Shape is within 25 meters visible to the camera
----end
----```
----@param handle number Shape handle
----@param maxDist number Maximum visible distance
----@param rejectTransparent boolean See through transparent materials. Default false.
----@return boolean visible Return true if shape is visible
-function IsShapeVisible(handle, maxDist, rejectTransparent) end
-
----Determine if shape has been broken. Note that a shape can be transfered
----to another body during destruction, but might still not be considered
----broken if all voxels are intact.
---- 
---- ---
---- Example
----```lua
----local broken = IsShapeBroken(shape)
----```
----@param handle number Shape handle
----@return boolean broken Return true if shape is broken
-function IsShapeBroken(handle) end
-
----Render next frame with an outline around specified shape.
----If no color is given, a white outline will be drawn.
---- 
---- ---
---- Example
----```lua
------Draw white outline at 50% transparency
----DrawShapeOutline(shape, 0.5)
----
------Draw green outline, fully opaque
----DrawShapeOutline(shape, 0, 1, 0, 1)
----```
----@param handle number Shape handle
----@param r number Red
----@param g number Green
----@param b number Blue
----@param a number Alpha
-function DrawShapeOutline(handle, r, g, b, a) end
-
----Flash the appearance of a shape when rendering this frame.
---- 
---- ---
---- Example
----```lua
----DrawShapeHighlight(shape, 0.5)
----```
----@param handle number Shape handle
----@param amount number Amount
-function DrawShapeHighlight(handle, amount) end
-
----This is used to filter out collisions with other shapes. Each shape can be given a layer 
----bitmask (8 bits, 0-255) along with a mask (also 8 bits). The layer of one object must be in
----the mask of the other object and vice versa for the collision to be valid. The default layer
----for all objects is 1 and the default mask is 255 (collide with all layers).
---- 
---- ---
---- Example
----```lua
------This will put shapes a and b in layer 2 and disable collisions with
------object shapes in layers 2, preventing any collisions between the two.
----SetShapeCollisionFilter(a, 2, 255-2)
----SetShapeCollisionFilter(b, 2, 255-2)
----
------This will put shapes c and d in layer 4 and allow collisions with other
------shapes in layer 4, but ignore all other collisions with the rest of the world.
----SetShapeCollisionFilter(c, 4, 4)
----SetShapeCollisionFilter(d, 4, 4)
----```
----@param handle number Shape handle
----@param layer number Layer bits (0-255)
----@param mask number Mask bits (0-255)
-function SetShapeCollisionFilter(handle, layer, mask) end
-
----This will return the closest point of a specific shape
---- 
---- ---
---- Example
----```lua
----local hit, p, n = GetShapeClosestPoint(s, Vec(0, 5, 0))
----if hit then
----	--Point p of shape s is closest to (0,5,0)
----end
----```
----@param shape number Shape handle
----@param origin table World space point
----@return boolean hit True if a point was found
----@return table point World space closest point
----@return table normal World space normal at closest point
-function GetShapeClosestPoint(shape, origin) end
-
----This will check if two shapes has physical overlap
---- 
---- ---
---- Example
----```lua
----local touch = IsShapeTouching(a, b)
----if hit then
----	--Shapes are touching or overlapping
----end
----```
----@param a number Handle to first shape
----@param b number Handle to second shape
----@return boolean touching True is shapes a and b are touching each other
-function IsShapeTouching(a, b) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local loc = FindLocation("start")
----```
----@param tag string Tag name
----@param global boolean Search in entire scene
----@return number handle Handle to first location with specified tag or zero if not found
-function FindLocation(tag, global) end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Search for locations tagged "waypoint" in script scope
----local locations = FindLocations("waypoint")
----for i=1, #locs do
----	local locs = locations[i]
----	...
----end
----```
----@param tag string Tag name
----@param global boolean Search in entire scene
----@return table list Indexed table with handles to all locations with specified tag
-function FindLocations(tag, global) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local t = GetLocationTransform(loc)
----```
----@param handle number Location handle
----@return table transform Transform of the location
-function GetLocationTransform(handle) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local joint = FindJoint("doorhinge")
----```
----@param tag string Tag name
----@param global boolean Search in entire scene
----@return number handle Handle to first joint with specified tag or zero if not found
-function FindJoint(tag, global) end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Search for locations tagged "doorhinge" in script scope
----local hinges = FindJoints("doorhinge")
----for i=1, #hinges do
----	local joint = hinges[i]
----	...
----end
----```
----@param tag string Tag name
----@param global boolean Search in entire scene
----@return table list Indexed table with handles to all joints with specified tag
-function FindJoints(tag, global) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local broken = IsJointBroken(joint)
----```
----@param joint number Joint handle
----@return boolean broken True if joint is broken
-function IsJointBroken(joint) end
-
----Joint type is one of the following: "ball", "hinge", "prismatic" or "rope".
----An empty string is returned if joint handle is invalid.
---- 
---- ---
---- Example
----```lua
----if GetJointType(joint) == "rope" then
----	--Joint is rope
----end
----```
----@param joint number Joint handle
----@return string type Joint type
-function GetJointType(joint) end
-
----A joint is always connected to two shapes. Use this function if you know 
----one shape and want to find the other one.
---- 
---- ---
---- Example
----```lua
------joint is connected to a and b
----
----otherShape = GetJointOtherShape(joint, a)
------otherShape is now b
----
----otherShape = GetJointOtherShape(joint, b)
------otherShape is now a
----```
----@param joint number Joint handle
----@param shape number Shape handle
----@return number other Other shape handle
-function GetJointOtherShape(joint, shape) end
-
----Set joint motor target velocity. If joint is of type hinge, velocity is
----given in radians per second angular velocity. If joint type is prismatic joint
----velocity is given in meters per second. Calling this function will override and
----void any previous call to SetJointMotorTarget.
---- 
---- ---
---- Example
----```lua
------Set motor speed to 0.5 radians per second
----SetJointMotor(hinge, 0.5)
----```
----@param joint number Joint handle
----@param velocity number Desired velocity
----@param strength number Desired strength. Default is infinite. Zero to disable.
-function SetJointMotor(joint, velocity, strength) end
-
----If a joint has a motor target, it will try to maintain its relative movement. This
----is very useful for elevators or other animated, jointed mechanisms.
----If joint is of type hinge, target is an angle in degrees (-180 to 180) and velocity
----is given in radians per second. If joint type is prismatic, target is given
----in meters and velocity is given in meters per second. Setting a motor target will
----override any previous call to SetJointMotor.
---- 
---- ---
---- Example
----```lua
------Make joint reach a 45 degree angle, going at a maximum of 3 radians per second
----SetJointMotorTarget(hinge, 45, 3)
----```
----@param joint number Joint handle
----@param target number Desired movement target
----@param maxVel number Maximum velocity to reach target. Default is infinite.
----@param strength number Desired strength. Default is infinite. Zero to disable.
-function SetJointMotorTarget(joint, target, maxVel, strength) end
-
----Return joint limits for hinge or prismatic joint. Returns angle or distance
----depending on joint type.
---- 
---- ---
---- Example
----```lua
----local min, max = GetJointLimits(hinge)
----```
----@param joint number Joint handle
----@return number min Minimum joint limit (angle or distance)
----@return number max Maximum joint limit (angle or distance)
-function GetJointLimits(joint) end
-
----Return the current position or angle or the joint, measured in same way
----as joint limits.
---- 
---- ---
---- Example
----```lua
----local current = GetJointMovement(hinge)
----```
----@param joint number Joint handle
----@return number movement Current joint position or angle
-function GetJointMovement(joint) end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Draw outline for all bodies in jointed structure
----local all = GetJointedDynamicBodies(body)
----for i=1,#all do
----	DrawBodyOutline(all[i], 0.5)
----end
----```
----@param body number Body handle (must be dynamic)
----@return table bodies Handles to all dynamic bodies in the jointed structure. The input handle will also be included.
-function GetJointedBodies(body) end
-
----Detach joint from shape. If joint is not connected to shape, nothing happens.
---- 
---- ---
---- Example
----```lua
----DetachJointFromShape(hinge, door)
----```
----@param joint number Joint handle
----@param shape number Shape handle
-function DetachJointFromShape(joint, shape) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local light = FindLight("main")
----```
----@param tag string Tag name
----@param global boolean Search in entire scene
----@return number handle Handle to first light with specified tag or zero if not found
-function FindLight(tag, global) end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Search for lights tagged "main" in script scope
----local lights = FindLights("main")
----for i=1, #lights do
----	local light = lights[i]
----	...
----end
----```
----@param tag string Tag name
----@param global boolean Search in entire scene
----@return table list Indexed table with handles to all lights with specified tag
-function FindLights(tag, global) end
-
----If light is owned by a shape, the emissive scale of that shape will be set
----to 0.0 when light is disabled and 1.0 when light is enabled.
---- 
---- ---
---- Example
----```lua
----SetLightEnabled(light, false)
----```
----@param handle number Light handle
----@param enabled boolean Set to true if light should be enabled
-function SetLightEnabled(handle, enabled) end
-
----This will only set the color tint of the light. Use SetLightIntensity for brightness.
----Setting the light color will not affect the emissive color of a parent shape.
---- 
---- ---
---- Example
----```lua
------Set light color to yellow
----SetLightColor(light, 1, 1, 0)
----```
----@param handle number Light handle
----@param r number Red value
----@param g number Green value
----@param b number Blue value
-function SetLightColor(handle, r, g, b) end
-
----If the shape is owned by a shape you most likely want to use
----SetShapeEmissiveScale instead, which will affect both the emissiveness 
----of the shape and the brightness of the light at the same time.
---- 
---- ---
---- Example
----```lua
------Pulsate light
----SetLightIntensity(light, math.sin(GetTime())*0.5 + 1.0)
----```
----@param handle number Light handle
----@param intensity number Desired intensity of the light
-function SetLightIntensity(handle, intensity) end
-
----Lights that are owned by a dynamic shape are automatcially moved with that shape
---- 
---- ---
---- Example
----```lua
----local pos = GetLightTransform(light).pos
----```
----@param handle number Light handle
----@return table transform World space light transform
-function GetLightTransform(handle) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local shape = GetLightShape(light)
----```
----@param handle number Light handle
----@return number handle Shape handle or zero if not attached to shape
-function GetLightShape(handle) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----if IsLightActive(light) then
----	--Do something
----end
----```
----@param handle number Light handle
----@return boolean active True if light is currently emitting light
-function IsLightActive(handle) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local point = Vec(0, 10, 0)
----local affected = IsPointAffectedByLight(light, point)
----```
----@param handle number Light handle
----@param point table World space point as vector
----@return boolean affected Return true if point is in light cone and range
-function IsPointAffectedByLight(handle, point) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local goal = FindTrigger("goal")
----```
----@param tag string Tag name
----@param global boolean Search in entire scene
----@return number handle Handle to first trigger with specified tag or zero if not found
-function FindTrigger(tag, global) end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Find triggers tagged "toxic" in script scope
----local triggers = FindTriggers("toxic")
----for i=1, #triggers do
----	local trigger = triggers[i]
----	...
----end
----```
----@param tag string Tag name
----@param global boolean Search in entire scene
----@return table list Indexed table with handles to all triggers with specified tag
-function FindTriggers(tag, global) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local t = GetTriggerTransform(trigger)
----```
----@param handle number Trigger handle
----@return table transform Current trigger transform in world space
-function GetTriggerTransform(handle) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local t = Transform(Vec(0, 1, 0), QuatEuler(0, 90, 0))
----SetTriggerTransform(trigger, t)
----```
----@param handle number Trigger handle
----@param transform table Desired trigger transform in world space
-function SetTriggerTransform(handle, transform) end
-
----Return the lower and upper points in world space of the trigger axis aligned bounding box
---- 
---- ---
---- Example
----```lua
----local mi, ma = GetTriggerBounds(trigger)
----local list = QueryAabbShapes(mi, ma)
----```
----@param handle number Trigger handle
----@return table min Lower point of trigger bounds in world space
----@return table max Upper point of trigger bounds in world space
-function GetTriggerBounds(handle) end
-
----This function will only check the center point of the body
---- 
---- ---
---- Example
----```lua
----if IsBodyInTrigger(trigger, body) then
----	...
----end
----```
----@param trigger number Trigger handle
----@param body number Body handle
----@return boolean inside True if body is in trigger volume
-function IsBodyInTrigger(trigger, body) end
-
----This function will only check origo of vehicle
---- 
---- ---
---- Example
----```lua
----if IsVehicleInTrigger(trigger, vehicle) then
----	...
----end
----```
----@param trigger number Trigger handle
----@param vehicle number Vehicle handle
----@return boolean inside True if vehicle is in trigger volume
-function IsVehicleInTrigger(trigger, vehicle) end
-
----This function will only check the center point of the shape
---- 
---- ---
---- Example
----```lua
----if IsShapeInTrigger(trigger, shape) then
----	...
----end
----```
----@param trigger number Trigger handle
----@param shape number Shape handle
----@return boolean inside True if shape is in trigger volume
-function IsShapeInTrigger(trigger, shape) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local p = Vec(0, 10, 0)
----if IsPointInTrigger(trigger, p) then
----	...
----end
----```
----@param trigger number Trigger handle
----@param point table Word space point as vector
----@return boolean inside True if point is in trigger volume
-function IsPointInTrigger(trigger, point) end
-
----This function will check if trigger is empty. If trigger contains any part of a body
----it will return false and the highest point as second return value.
---- 
---- ---
---- Example
----```lua
----local empty, highPoint = IsTriggerEmpty(trigger)
----if not empty then
----	--highPoint[2] is the tallest point in trigger
----end
----```
----@param handle number Trigger handle
----@param demolision boolean If true, small debris and vehicles are ignored
----@return boolean empty True if trigger is empty
----@return table maxpoint World space point of highest point (largest Y coordinate) if not empty
-function IsTriggerEmpty(handle, demolision) end
-
----Get distance to the surface of trigger volume. Will return negative distance if inside.
---- 
---- ---
---- Example
----```lua
----local p = Vec(0, 10, 0)
----local dist = GetTriggerDistance(trigger, p)
----```
----@param trigger number Trigger handle
----@param point table Word space point as vector
----@return number distance Positive if point is outside, negative if inside
-function GetTriggerDistance(trigger, point) end
-
----Return closest point in trigger volume. Will return the input point itself if inside trigger
----or closest point on surface of trigger if outside.
---- 
---- ---
---- Example
----```lua
----local p = Vec(0, 10, 0)
----local closest = GetTriggerClosestPoint(trigger, p)
----```
----@param trigger number Trigger handle
----@param point table Word space point as vector
----@return table closest Closest point in trigger as vector
-function GetTriggerClosestPoint(trigger, point) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local screen = FindTrigger("tv")
----```
----@param tag string Tag name
----@param global boolean Search in entire scene
----@return number handle Handle to first screen with specified tag or zero if not found
-function FindScreen(tag, global) end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Find screens tagged "tv" in script scope
----local screens = FindScreens("tv")
----for i=1, #screens do
----	local screen = screens[i]
----	...
----end
----```
----@param tag string Tag name
----@param global boolean Search in entire scene
----@return table list Indexed table with handles to all screens with specified tag
-function FindScreens(tag, global) end
-
----Enable or disable screen
---- 
---- ---
---- Example
----```lua
----SetScreenEnabled(screen, true)
----```
----@param screen number Screen handle
----@param enabled boolean True if screen should be enabled
-function SetScreenEnabled(screen, enabled) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local b = IsScreenEnabled(screen)
----```
----@param screen number Screen handle
----@return boolean enabled True if screen is enabled
-function IsScreenEnabled(screen) end
-
----Return handle to the parent shape of a screen
---- 
---- ---
---- Example
----```lua
----local shape = GetScreenShape(screen)
----```
----@param screen number Screen handle
----@return number shape Shape handle or zero if none
-function GetScreenShape(screen) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local vehicle = FindVehicle("mycar")
----```
----@param tag string Tag name
----@param global boolean Search in entire scene
----@return number handle Handle to first vehicle with specified tag or zero if not found
-function FindVehicle(tag, global) end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Find all vehicles in level tagged "boat"
----local boats = FindVehicles("boat")
----for i=1, #boats do
----	local boat = boats[i]
----	...
----end
----```
----@param tag string Tag name
----@param global boolean Search in entire scene
----@return table list Indexed table with handles to all vehicles with specified tag
-function FindVehicles(tag, global) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local t = GetVehicleTransform(vehicle)
----```
----@param vehicle number Vehicle handle
----@return table transform Transform of vehicle
-function GetVehicleTransform(vehicle) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local body = GetVehicleBody(vehicle)
----if IsBodyBroken(body) then
------Vehicle body is broken
----end
----```
----@param vehicle number Vehicle handle
----@return number body Main body of vehicle
-function GetVehicleBody(vehicle) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local health = GetVehicleHealth(vehicle)
----```
----@param vehicle number Vehicle handle
----@return number health Vehicle health (zero to one)
-function GetVehicleHealth(vehicle) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local driverPos = GetVehicleDriverPos(vehicle)
----local t = GetVehicleTransform(vehicle)
----local worldPos = TransformToParentPoint(t, driverPos)
----```
----@param vehicle number Vehicle handle
----@return table pos Driver position as vector in vehicle space
-function GetVehicleDriverPos(vehicle) end
-
----This function applies input to vehicles, allowing for autonomous driving. The vehicle
----will be turned on automatically and turned off when no longer called. Call this from
----the tick function, not update.
---- 
---- ---
---- Example
----```lua
----function tick()
----	--Drive mycar forwards
----	local v = FindVehicle("mycar")
----	DriveVehicle(v, 1, 0, false)
----end
----```
----@param vehicle number Vehicle handle
----@param drive number Reverse/forward control -1 to 1
----@param steering number Left/right control -1 to 1
----@param handbrake boolean Handbrake control
-function DriveVehicle(vehicle, drive, steering, handbrake) end
-
----Return center point of player. This function is deprecated. 
----Use GetPlayerTransform instead.
---- 
---- ---
---- Example
----```lua
----local p = GetPlayerPos()
----
------This is equivalent to
----p = VecAdd(GetPlayerTransform().pos, Vec(0,1,0))
----```
----@return table position Player center position
-function GetPlayerPos() end
-
----The player transform is located at the bottom of the player. The player transform
----considers heading (looking left and right). Forward is along negative Z axis.
----Player pitch (looking up and down) does not affect player transform unless includePitch
----is set to true. If you want the transform of the eye, use GetPlayerCameraTransform() instead.
---- 
---- ---
---- Example
----```lua
----local t = GetPlayerTransform()
----```
----@param includePitch boolean Include the player pitch (look up/down) in transform
----@return table transform Current player transform
-function GetPlayerTransform(includePitch) end
-
----Instantly teleport the player to desired transform. Unless includePitch is
----set to true, up/down look angle will be set to zero during this process.
----Player velocity will be reset to zero.
---- 
---- ---
---- Example
----```lua
----local t = Transform(Vec(10, 0, 0), QuatEuler(0, 90, 0))
----SetPlayerTransform(t)
----```
----@param transform table Desired player transform
----@param includePitch boolean Set player pitch (look up/down) as well
-function SetPlayerTransform(transform, includePitch) end
-
----Make the ground act as a conveyor belt, pushing the player even if ground shape is static.
---- 
---- ---
---- Example
----```lua
----SetPlayerGroundVelocity(Vec(2,0,0))
----```
----@param vel table Desired ground velocity
-function SetPlayerGroundVelocity(vel) end
-
----The player camera transform is usually the same as what you get from GetCameraTransform,
----but if you have set a camera transform manually with SetCameraTransform, you can retrieve
----the standard player camera transform with this function.
---- 
---- ---
---- Example
----```lua
----local t = GetPlayerCameraTransform()
----```
----@return table transform Current player camera transform
-function GetPlayerCameraTransform() end
-
----Call this function during init to alter the player spawn transform.
---- 
---- ---
---- Example
----```lua
----local t = Transform(Vec(10, 0, 0), QuatEuler(0, 90, 0))
----SetPlayerSpawnTransform(t)
----```
----@param transform table Desired player spawn transform
-function SetPlayerSpawnTransform(transform) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local vel = GetPlayerVelocity()
----```
----@return table velocity Player velocity in world space as vector
-function GetPlayerVelocity() end
-
----Drive specified vehicle.
---- 
---- ---
---- Example
----```lua
----local car = FindVehicle("mycar")
----SetPlayerVehicle(car)
----```
----@param vehicle number Handle to vehicle or zero to not drive.
-function SetPlayerVehicle(vehicle) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----SetPlayerVelocity(Vec(0, 5, 0))
----```
----@param velocity table Player velocity in world space as vector
-function SetPlayerVelocity(velocity) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local vehicle = GetPlayerVehicle()
----if vehicle ~= 0 then
----	...
----end
----```
----@return number handle Current vehicle handle, or zero if not in vehicle
-function GetPlayerVehicle() end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local shape = GetPlayerGrabShape()
----if shape ~= 0 then
----	...
----end
----```
----@return number handle Handle to grabbed shape or zero if not grabbing.
-function GetPlayerGrabShape() end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local body = GetPlayerGrabBody()
----if body ~= 0 then
----	...
----end
----```
----@return number handle Handle to grabbed body or zero if not grabbing.
-function GetPlayerGrabBody() end
-
----Release what the player is currently holding
---- 
---- ---
---- Example
----```lua
----ReleasePlayerGrab()
----```
-function ReleasePlayerGrab() end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local shape = GetPlayerPickShape()
----if shape ~= 0 then
----	...
----end
----```
----@return number handle Handle to picked shape or zero if nothing is picked
-function GetPlayerPickShape() end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local body = GetPlayerPickBody()
----if body ~= 0 then
----	...
----end
----```
----@return number handle Handle to picked body or zero if nothing is picked
-function GetPlayerPickBody() end
-
----Interactable shapes has to be tagged with "interact". The engine
----determines which interactable shape is currently interactable.
---- 
---- ---
---- Example
----```lua
----local shape = GetPlayerInteractShape()
----if shape ~= 0 then
----	...
----end
----```
----@return number handle Handle to interactable shape or zero
-function GetPlayerInteractShape() end
-
----Interactable shapes has to be tagged with "interact". The engine
----determines which interactable body is currently interactable.
---- 
---- ---
---- Example
----```lua
----local body = GetPlayerInteractBody()
----if body ~= 0 then
----	...
----end
----```
----@return number handle Handle to interactable body or zero
-function GetPlayerInteractBody() end
-
----Set the screen the player should interact with. For the screen
----to feature a mouse pointer and receieve input, the screen also
----needs to have interactive property.
---- 
---- ---
---- Example
----```lua
------Interact with screen
----SetPlayerScreen(screen)
----
------Do not interact with screen
----SetPlayerScreen(0)
----```
----@param handle number Handle to screen or zero for no screen
-function SetPlayerScreen(handle) end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Interact with screen
----local screen = GetPlayerScreen()
----```
----@return number handle Handle to interacted screen or zero if none
-function GetPlayerScreen() end
-
----No Description
---- 
---- ---
---- Example
----```lua
----SetPlayerHealth(0.5)
----```
----@param health number Set player health (between zero and one)
-function SetPlayerHealth(health) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local health = GetPlayerHealth()
----```
----@return number health Current player health
-function GetPlayerHealth() end
-
----Respawn player at spawn position without modifying the scene
---- 
---- ---
---- Example
----```lua
----RespawnPlayer()
----```
-function RespawnPlayer() end
-
----Register a custom tool that will show up in the player inventory and 
----can be selected with scroll wheel. Do this only once per tool.
----You also need to enable the tool in the registry before it can be used.
---- 
---- ---
---- Example
----```lua
----function init()
----	RegisterTool("lasergun", "Laser Gun", "MOD/vox/lasergun.vox")
----	SetBool("game.tool.lasergun.enabled", true)
----end
----
----function tick()
----	if GetString("game.player.tool") == "lasergun" then
----		--Tool is selected. Tool logic goes here.
----	end
----end
----```
----@param id string Tool unique identifier
----@param name string Tool name to show in hud
----@param file string Path to vox file
----@param group number Tool group for this tool (1-6) Default is 6.
-function RegisterTool(id, name, file, group) end
-
----Return body handle of the visible tool. You can use this to retrieve tool shapes
----and animate them, change emissiveness, etc. Do not attempt to set the tool body
----transform, since it is controlled by the engine. Use SetToolTranform for that.
---- 
---- ---
---- Example
----```lua
----local toolBody = GetToolBody()
----if toolBody~=0 then
----	...
----end
----```
----@return number handle Handle to currently visible tool body or zero if none
-function GetToolBody() end
-
----Apply an additional transform on the visible tool body. This can be used to
----create tool animations. You need to set this every frame from the tick function.
----The optional sway parameter control the amount of tool swaying when walking.
----Set to zero to disable completely.
---- 
---- ---
---- Example
----```lua
------Offset the tool half a meter to the right
----local offset = Transform(Vec(0.5, 0, 0))
----SetToolTransform(offset)
----```
----@param transform table Tool body transform
----@param sway number Tool sway amount. Default is 1.0.
-function SetToolTransform(transform, sway) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local snd = LoadSound("beep.ogg")
----```
----@param path string Path to ogg sound file
----@param nominalDistance number The distance in meters this sound is recorded at. Affects attenuation, default is 10.0
----@return number handle Sound handle
-function LoadSound(path, nominalDistance) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local loop = LoadLoop("siren.ogg")
----```
----@param path string Path to ogg sound file
----@param nominalDistance number The distance in meters this sound is recorded at. Affects attenuation, default is 10.0
----@return number handle Loop handle
-function LoadLoop(path, nominalDistance) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----function init()
----	snd = LoadSound("beep.ogg")
----end
----
----function tick()
----	if trigSound then
----		local pos = Vec(100, 0, 0)
----		PlaySound(snd, pos, 0.5)
----	end
----end
----```
----@param handle number Sound handle
----@param pos table World position as vector. Default is player position.
----@param volume number Playback volume. Default is 1.0
-function PlaySound(handle, pos, volume) end
-
----Call this function continuously to play loop
---- 
---- ---
---- Example
----```lua
----function init()
----	loop = LoadLoop("siren.ogg")
----end
----
----function tick()
----	local pos = Vec(100, 0, 0)
----	PlayLoop(loop, pos, 0.5)
----end
----```
----@param handle number Loop handle
----@param pos table World position as vector. Default is player position.
----@param volume number Playback volume. Default is 1.0
-function PlayLoop(handle, pos, volume) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----PlayMusic("MOD/music/background.ogg")
----```
----@param path string Music path
-function PlayMusic(path) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----StopMusic()
----```
-function StopMusic() end
-
----No Description
---- 
---- ---
---- Example
----```lua
----function init()
----	arrow = LoadSprite("arrow.png")
----end
----```
----@param path string Path to sprite. Must be PNG or JPG format.
----@return number handle Sprite handle
-function LoadSprite(path) end
-
----Draw sprite in world at next frame. Call this function from the tick callback.
---- 
---- ---
---- Example
----```lua
----function init()
----	arrow = LoadSprite("arrow.png")
----end
----
----function tick()
----	--Draw sprite using transform
----	--Size is two meters in width and height
----	--Color is white, fully opaue
----	local t = Transform(Vec(0, 10, 0), QuatEuler(0, GetTime(), 0))
----	DrawSprite(arrow, t, 2, 2, 1, 1, 1, 1)
----end
----```
----@param handle number Sprite handle
----@param transform table Transform
----@param width number Width in meters
----@param height number Height in meters
----@param r number Red color. Default 1.0.
----@param g number Green color. Default 1.0.
----@param b number Blue color. Default 1.0.
----@param a number Alpha. Default 1.0.
----@param depthTest boolean Depth test enabled. Default false.
----@param additive boolean Additive blending enabled. Default false.
-function DrawSprite(handle, transform, width, height, r, g, b, a, depthTest, additive) end
-
----Set required layers for next query. Available layers are:
----
----Layer  Description
----physical	 have a physical representationdynamic		 part of a dynamic bodystatic		 part of a static bodylarge		 above debris thresholdsmall		 below debris threshold
---- 
---- ---
---- Example
----```lua
------Raycast dynamic, physical objects above debris threshold, but not specific vehicle
----QueryRequire("physical dynamic large")
----QueryRejectVehicle(vehicle)
+---
+
+er position.
+---@param volume number Playbac
+
+sition.
+---@param volume number Playback vo
+
+ow = LoadSprite("arrow.png")
+---end
+---```
+
+-Draw sprite in world at nex
+
+-```lua
+---function init
+
+(0, GetTime(), 0))
+---	DrawSp
+
+amic, physical objects above debris threshold, but not specific vehicle
+---QueryRequire("p
+
+ycast
+---QueryRejectBody(body)
+--
+
+ectShape(shape)
 ---QueryRaycast(...)
----```
----@param layers string Space separate list of layers
-function QueryRequire(layers) end
-
----Exclude vehicle from the next query
---- 
---- ---
---- Example
----```lua
------Do not include vehicle in next raycast
----QueryRejectVehicle(vehicle)
----QueryRaycast(...)
----```
----@param vehicle number Vehicle handle
-function QueryRejectVehicle(vehicle) end
-
----Exclude body from the next query
---- 
---- ---
---- Example
----```lua
------Do not include body in next raycast
----QueryRejectBody(body)
----QueryRaycast(...)
----```
----@param body number Body handle
-function QueryRejectBody(body) end
-
----Exclude shape from the next query
---- 
---- ---
---- Example
----```lua
------Do not include shape in next raycast
----QueryRejectShape(shape)
----QueryRaycast(...)
----```
----@param shape number Shape handle
-function QueryRejectShape(shape) end
-
----This will perform a raycast or spherecast (if radius is more than zero) query.
----If you want to set up a filter for the query you need to do so before every call
----to this function.
---- 
---- ---
---- Example
----```lua
------Raycast from a high point straight downwards, excluding a specific vehicle
----QueryRejectVehicle(vehicle)
----local hit, d = QueryRaycast(Vec(0, 100, 0), Vec(0, -1, 0), 100)
----if hit then
----	...hit something at distance d
----end
----```
----@param origin table Raycast origin as world space vector
----@param direction table Unit length raycast direction as world space vector
----@param maxDist number Raycast maximum distance. Keep this as low as possible for good performance.
----@param radius number Raycast thickness. Default zero.
----@param rejectTransparent boolean Raycast through transparent materials. Default false.
----@return boolean hit True if raycast hit something
----@return number dist Hit distance from origin
----@return table normal World space normal at hit point
----@return number shape Handle to hit shape
-function QueryRaycast(origin, direction, maxDist, radius, rejectTransparent) end
-
----This will query the closest point to all shapes in the world. If you 
----want to set up a filter for the query you need to do so before every call
----to this function.
---- 
---- ---
---- Example
----```lua
------Find closest point within 10 meters of {0, 5, 0}, excluding any point on myVehicle
----QueryRejectVehicle(myVehicle)
+---
+
+uery you need to do so before ever
+
+0, 100, 0), Vec(0, -1, 0), 100)
+---i
+
 ---local hit, p, n, s = QueryClosestPoint(Vec(0, 5, 0), 10)
 ---if hit then
----	--Point p of shape s is closest
----end
----```
----@param origin table World space point
----@param maxDist number Maximum distance. Keep this as low as possible for good performance.
----@return boolean hit True if a point was found
----@return table point World space closest point
----@return table normal World space normal at closest point
----@return number shape Handle to closest shape
-function QueryClosestPoint(origin, maxDist) end
-
----Return all shapes within the provided world space, axis-aligned bounding box
---- 
---- ---
---- Example
----```lua
----local list = QueryAabbShapes(Vec(0, 0, 0), Vec(10, 10, 10))
----for i=1, #list do
----	local shape = list[i]
----	..
----end
----```
+---	
+
+ith handles to all shapes in the aabb
+function 
+
+to all bodies in the aabb
+function Que
+
+able World space start point
+---@param
+
+	 No recent querybusy	 Busy computing. No path found yet.
+
+al s = GetPathState()
+--
+
+function GetPathLength() en
+
+d + 0.5
+---end
+---```
+---@pa
+
+nt d meters into water
+---end
+-
+
+provided point. The wind wi
+
+le state, which is a plain, white 
+
+ction ParticleType(type) end
+
+---No
+
+n ParticleTile(type) end
+
+--
+
+olor(1,0,0)
+---
+-----Animating 
+
+en value at end
+---@param b1 nu
+
+ Default is linear.
+---@param fadein number Fade i
+
+de in between t=0 and t=fadein. Default is zero.
+---@param fadeout 
+
+Default is linear.
+---@param fadein number Fade in between t=0 and
+
+Interpolation method: linear, smooth, easein, easeout or constant. D
+
+.
+---@param fadein number Fade in between t=0 and t=fadein. Defau
+
+sein, easeout or constant. Default is linear.
+---@param fadein number
+
+rpolation method: linear, smooth, easein, easeout or constant. Defaul
+
+---@param fadein number Fade in between t=0 and t=fadein. Default i
+
+amp up collisions very quickly, only skipping the first 5% of lifet
+
+ask) end
+
+---Spawn particle using the previously set up particle sta
+
+ld origo with upwards velocity and 
+
+ Transform(Vec(0, 5, 0)))
+---Spawn("<voxbox size='1
+
+, direction, type, strength) end
+
+---Make a hole in the enviro
+
+umber Hole radius for medium materials. May not be bi
+
+iption
+--- 
+--- ---
+--- Example
+---```lua
+---local 
+
+etPlayerTransform().pos, 5.0)
+---
+
+ble World space position as
+
+n of closest fire
+function 
+
+-```
 ---@param min table Aabb minimum point
----@param max table Aabb maximum point
----@return table list Indexed table with handles to all shapes in the aabb
-function QueryAabbShapes(min, max) end
-
----Return all bodies within the provided world space, axis-aligned bounding box
---- 
---- ---
---- Example
----```lua
----local list = QueryAabbBodies(Vec(0, 0, 0), Vec(10, 10, 10))
----for i=1, #list do
----	local body = list[i]
----	..
----end
----```
----@param min table Aabb minimum point
----@param max table Aabb maximum point
----@return table list Indexed table with handles to all bodies in the aabb
-function QueryAabbBodies(min, max) end
-
----Initiate path planning query. The result will run asynchronously as long as GetPathState
----retuns "busy". An ongoing path query can be aborted with AbortPath. The path planning query
----will use the currently set up query filter, just like the other query functions.
---- 
---- ---
---- Example
----```lua
----QueryPath(Vec(-10, 0, 0), Vec(10, 0, 0))
----```
----@param start table World space start point
----@param end table World space target point
----@param maxDist number Maximum path length before giving up. Default is infinite.
----@param targetRadius number Maximum allowed distance to target in meters. Default is 2.0
-function QueryPath(start, end, maxDist, targetRadius) end
-
----Abort current path query, regardless of what state it is currently in. This is a way to
----save computing resources if the result of the current query is no longer of interest.
---- 
---- ---
---- Example
----```lua
----AbortPath()
----```
-function AbortPath() end
-
----Return the current state of the last path planning query.
----
----State  Description
----idle	 No recent querybusy	 Busy computing. No path found yet.fail	 Failed to find path. You can still get the resulting path (even though it won't reach the target).done	 Path planning completed and a path was found. Get it with GetPathLength and GetPathPoint)
---- 
---- ---
---- Example
----```lua
----local s = GetPathState()
----if s == "done" then
----	DoSomething()
----end
----```
----@return string state Current path planning state
-function GetPathState() end
-
----Return the path length of the most recently computed path query. Note that the result can often be retrieved even
----if the path query failed. If the target point couldn't be reached, the path endpoint will be the point closest
----to the target.
---- 
---- ---
---- Example
----```lua
----local l = GetPathLength()
----```
----@return number length Length of last path planning result (in meters)
-function GetPathLength() end
-
----Return a point along the path for the most recently computed path query. Note that the result can often be retrieved even
----if the path query failed. If the target point couldn't be reached, the path endpoint will be the point closest
----to the target.
---- 
---- ---
---- Example
----```lua
----local d = 0
----local l = GetPathLength()
----while d < l do
----	DebugCross(GetPathPoint(d))
----	d = d + 0.5
----end
----```
----@param dist number The distance along path. Should be between zero and result from GetPathLength()
----@return table point The path point dist meters along the path
-function GetPathPoint(dist) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local vol, pos = GetLastSound()
----```
----@return number volume Volume of loudest sound played last frame
----@return table position World position of loudest sound played last frame
-function GetLastSound() end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local wet, d = IsPointInWater(Vec(10, 0, 0))
----if wet then
----	...point d meters into water
----end
----```
----@param point table World point as vector
----@return boolean inWater True if point is in water
----@return number depth Depth of point into water, or zero if not in water
-function IsPointInWater(point) end
-
----Get the wind velocity at provided point. The wind will be determined by wind property of
----the environment, but it varies with position procedurally.
---- 
---- ---
---- Example
----```lua
----local v = GetWindVelocity(Vec(0, 10, 0))
----```
----@param point table World point as vector
----@return table vel Wind at provided position
-function GetWindVelocity(point) end
-
----Reset to default particle state, which is a plain, white particle of radius 0.5.
----Collision is enabled and it alpha animates from 1 to 0.
---- 
---- ---
---- Example
----```lua
----ParticleReset()
----```
-function ParticleReset() end
-
----Set type of particle
---- 
---- ---
---- Example
----```lua
----ParticleType("smoke")
----```
----@param type string Type of particle. Can be "smoke" or "plain".
-function ParticleType(type) end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Smoke particle
----ParticleTile(0)
----
------Fire particle
----ParticleTile(5)
----```
----@param type integer Tile in the particle texture atlas (0-15)
-function ParticleTile(type) end
-
----Set particle color to either constant (three arguments) or linear interpolation (six arguments)
---- 
---- ---
---- Example
----```lua
------Constant red
----ParticleColor(1,0,0)
----
------Animating from yellow to red
----ParticleColor(1,1,0, 1,0,0)
----```
----@param r0 number Red value
----@param g0 number Green value
----@param b0 number Blue value
----@param r1 number Red value at end
----@param g1 number Green value at end
----@param b1 number Blue value at end
-function ParticleColor(r0, g0, b0, r1, g1, b1) end
-
----Set the particle radius. Max radius for smoke particles is 1.0.
---- 
---- ---
---- Example
----```lua
------Constant radius 0.4 meters
----ParticleRadius(0.4)
----
------Interpolate from small to large
----ParticleRadius(0.1, 0.7)
----```
----@param r0 number Radius
----@param r1 number End radius
----@param interpolation string Interpolation method: linear, smooth, easein, easeout or constant. Default is linear.
----@param fadein number Fade in between t=0 and t=fadein. Default is zero.
----@param fadeout number Fade out between t=fadeout and t=1. Default is one.
-function ParticleRadius(r0, r1, interpolation, fadein, fadeout) end
-
----Set the particle alpha (opacity).
---- 
---- ---
---- Example
----```lua
------Interpolate from opaque to transparent
----ParticleAlpha(1.0, 0.0)
----```
----@param a0 number Alpha (0.0 - 1.0)
----@param a1 number End alpha (0.0 - 1.0)
----@param interpolation string Interpolation method: linear, smooth, easein, easeout or constant. Default is linear.
----@param fadein number Fade in between t=0 and t=fadein. Default is zero.
----@param fadeout number Fade out between t=fadeout and t=1. Default is one.
-function ParticleAlpha(a0, a1, interpolation, fadein, fadeout) end
-
----Set particle gravity. It will be applied along the world Y axis. A negative value will move the particle downwards.
---- 
---- ---
---- Example
----```lua
------Move particles slowly upwards
----ParticleGravity(2)
----```
----@param g0 number Gravity
----@param g1 number End gravity
----@param interpolation string Interpolation method: linear, smooth, easein, easeout or constant. Default is linear.
----@param fadein number Fade in between t=0 and t=fadein. Default is zero.
----@param fadeout number Fade out between t=fadeout and t=1. Default is one.
-function ParticleGravity(g0, g1, interpolation, fadein, fadeout) end
-
----Particle drag will slow down fast moving particles. It's implemented slightly different for
----smoke and plain particles. Drag must be positive, and usually look good between zero and one.
---- 
---- ---
---- Example
----```lua
------Sow down fast moving particles
----ParticleDrag(0.5)
----```
----@param d0 number Drag
----@param d1 number End drag
----@param interpolation string Interpolation method: linear, smooth, easein, easeout or constant. Default is linear.
----@param fadein number Fade in between t=0 and t=fadein. Default is zero.
----@param fadeout number Fade out between t=fadeout and t=1. Default is one.
-function ParticleDrag(d0, d1, interpolation, fadein, fadeout) end
-
----Draw particle as emissive (glow in the dark). This is useful for fire and embers.
---- 
---- ---
---- Example
----```lua
------Highly emissive at start, not emissive at end
----ParticleEmissive(5, 0)
----```
----@param d0 number Emissive
----@param d1 number End emissive
----@param interpolation string Interpolation method: linear, smooth, easein, easeout or constant. Default is linear.
----@param fadein number Fade in between t=0 and t=fadein. Default is zero.
----@param fadeout number Fade out between t=fadeout and t=1. Default is one.
-function ParticleEmissive(d0, d1, interpolation, fadein, fadeout) end
-
----Makes the particle rotate. Positive values is counter-clockwise rotation.
---- 
---- ---
---- Example
----```lua
------Rotate fast at start and slow at end
----ParticleEmissive(10, 1)
----```
----@param r0 number Rotation speed in radians per second.
----@param r1 number End rotation speed in radians per second.
----@param interpolation string Interpolation method: linear, smooth, easein, easeout or constant. Default is linear.
----@param fadein number Fade in between t=0 and t=fadein. Default is zero.
----@param fadeout number Fade out between t=fadeout and t=1. Default is one.
-function ParticleRotation(r0, r1, interpolation, fadein, fadeout) end
-
----Stretch particle along with velocity. 0.0 means no stretching. 1.0 stretches with the particle motion over
----one frame. Larger values stretches the particle even more.
---- 
---- ---
---- Example
----```lua
------Stretch particle along direction of motion
----ParticleStretch(1.0)
----```
----@param s0 number Stretch
----@param s1 number End stretch
----@param interpolation string Interpolation method: linear, smooth, easein, easeout or constant. Default is linear.
----@param fadein number Fade in between t=0 and t=fadein. Default is zero.
----@param fadeout number Fade out between t=fadeout and t=1. Default is one.
-function ParticleStretch(s0, s1, interpolation, fadein, fadeout) end
-
----Make particle stick when in contact with objects. This can be used for friction.
---- 
---- ---
---- Example
----```lua
------Make particles stick to objects
----ParticleSticky(0.5)
----```
----@param s0 number Sticky (0.0 - 1.0)
----@param s1 number End sticky (0.0 - 1.0)
----@param interpolation string Interpolation method: linear, smooth, easein, easeout or constant. Default is linear.
----@param fadein number Fade in between t=0 and t=fadein. Default is zero.
----@param fadeout number Fade out between t=fadeout and t=1. Default is one.
-function ParticleSticky(s0, s1, interpolation, fadein, fadeout) end
-
----Control particle collisions. A value of zero means that collisions are ignored. One means full collision.
----It is sometimes useful to animate this value from zero to one in order to not collide with objects around
----the emitter.
---- 
---- ---
---- Example
----```lua
------Disable collisions
----ParticleCollide(0)
----
------Enable collisions over time
----ParticleCollide(0, 1)
----
------Ramp up collisions very quickly, only skipping the first 5% of lifetime
----ParticleCollide(1, 1, "constant", 0.05)
----```
----@param c0 number Collide (0.0 - 1.0)
----@param c1 number End collide (0.0 - 1.0)
----@param interpolation string Interpolation method: linear, smooth, easein, easeout or constant. Default is linear.
----@param fadein number Fade in between t=0 and t=fadein. Default is zero.
----@param fadeout number Fade out between t=fadeout and t=1. Default is one.
-function ParticleCollide(c0, c1, interpolation, fadein, fadeout) end
-
----Set particle bitmask. The value 256 means fire extinguishing particles and is currently the only 
----flag in use. There might be support for custom flags and queries in the future.
---- 
---- ---
---- Example
----```lua
------Fire extinguishing particle
----ParticleFlags(256)
----SpawnParticle(...)
----```
----@param bitmask number Particle flags (bitmask 0-65535)
-function ParticleFlags(bitmask) end
-
----Spawn particle using the previously set up particle state. You can call this multiple times
----using the same particle state, but with different position, velocity and lifetime. You can
----also modify individual properties in the particle state in between calls to to this function.
---- 
---- ---
---- Example
----```lua
----ParticleReset()
----ParticleType("smoke")
----ParticleColor(0.7, 0.6, 0.5)
------Spawn particle at world origo with upwards velocity and a lifetime of ten seconds
----SpawnParticle(Vec(0, 0, 0), Vec(0, 1, 0), 10.0)
----```
----@param pos table World space point as vector
----@param velocity table World space velocity as vector
----@param lifetime number Particle lifetime in seconds
-function SpawnParticle(pos, velocity, lifetime) end
-
----The first argument can be either a prefab XML file in your mod folder or a string with XML content. It is also 
----possible to spawn prefabs from other mods, by using the mod id followed by colon, followed by the prefab path.
----Spawning prefabs from other mods should be used with causion since the referenced mod might not be installed.
---- 
---- ---
---- Example
----```lua
----Spawn("MOD/prefab/mycar.xml", Transform(Vec(0, 5, 0)))
----Spawn("<voxbox size='10 10 10' prop='true' material='wood'/>", Transform(Vec(0, 10, 0)))
----```
----@param xml string File name or xml string
----@param transform table Spawn transform
----@param allowStatic boolean Allow spawning static shapes and bodies (default false)
----@param jointExisting boolean Allow joints to connect to existing scene geometry (default false)
----@return table entities Indexed table with handles to all spawned entities
-function Spawn(xml, transform, allowStatic, jointExisting) end
-
----Shoot bullet or rocket (used for chopper)
---- 
---- ---
---- Example
----```lua
----Shoot(Vec(0, 10, 0), Vec(0, 0, 1))
----```
----@param origin table Origin in world space as vector
----@param direction table Unit length direction as world space vector
----@param type number 0 is regular bullet (default) and 1 is rocket
----@param strength number Projectile strength. Default is 1.
-function Shoot(origin, direction, type, strength) end
-
----Make a hole in the environment. Radius is given in meters. 
----Soft materials: glass, foliage, dirt, wood, plaster and plastic. 
----Medium materials: concrete, brick and weak metal. 
----Hard materials: hard metal and hard masonry.
---- 
---- ---
---- Example
----```lua
----MakeHole(pos, 1.2, 1.0)
----```
----@param position table Hole center point
----@param r0 number Hole radius for soft materials
----@param r1 number Hole radius for medium materials. May not be bigger than r0. Default zero.
----@param r2 number Hole radius for hard materials. May not be bigger than r1. Default zero.
----@param silent boolean Make hole without playing any break sounds.
----@return number count Number of voxels that was cut out. This will be zero if there were no changes to any shape.
-function MakeHole(position, r0, r1, r2, silent) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----Explosion(Vec(0, 10, 0), 1)
----```
----@param pos table Position in world space as vector
----@param size number Explosion size from 0.5 to 4.0
-function Explosion(pos, size) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----SpawnFire(Vec(0, 10, 0))
----```
----@param pos table Position in world space as vector
-function SpawnFire(pos) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local c = GetFireCount()
----```
----@return number count Number of active fires in level
-function GetFireCount() end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local hit, pos = QueryClosestFire(GetPlayerTransform().pos, 5.0)
----if hit then
----	--There is a fire within 5 meters to the player. Mark it with a debug cross.
----	DebugCross(pos)
----end
----```
----@param origin table World space position as vector
----@param maxDist number Maximum search distance
----@return boolean hit A fire was found within search distance
----@return table pos Position of closest fire
-function QueryClosestFire(origin, maxDist) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local count = QueryAabbFireCount(Vec(0,0,0), Vec(10,10,10))
----```
----@param min table Aabb minimum point
----@param max table Aabb maximum point
----@return number count Number of active fires in bounding box
-function QueryAabbFireCount(min, max) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local removedCount= RemoveAabbFires(Vec(0,0,0), Vec(10,10,10))
----```
----@param min table Aabb minimum point
----@param max table Aabb maximum point
----@return number count Number of fires removed
-function RemoveAabbFires(min, max) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local t = GetCameraTransform()
----```
----@return table transform Current camera transform
+--
+
+rm
 function GetCameraTransform() end
 
----Override current camera transform for this frame. Call continuously to keep overriding.
---- 
---- ---
---- Example
----```lua
----SetCameraTransform(Transform(Vec(0, 10, 0), QuatEuler(0, 90, 0)))
----```
----@param transform table Desired camera transform
----@param fov number Optional horizontal field of view in degrees (default: 90)
-function SetCameraTransform(transform, fov) end
-
----Override field of view for the next frame for all camera modes, except when explicitly set in SetCameraTransform
---- 
---- ---
---- Example
----```lua
----function tick()
----	SetCameraFov(60)
----end
----```
----@param degrees number Horizontal field of view in degrees (10-170)
-function SetCameraFov(degrees) end
-
----Override depth of field for the next frame for all camera modes. Depth of field will be used even if turned off in options.
---- 
---- ---
---- Example
----```lua
------Set depth of field to 10 meters
----SetCameraDof(10)
----```
----@param distance number Depth of field distance
----@param amount number Optional amount of blur (default 1.0)
-function SetCameraDof(distance, amount) end
-
----Add a temporary point light to the world for this frame. Call continuously
+---
+
+ram fov number Optional horizontal fie
+
+, except when explicitly set in S
+
+s.
+--- 
+--- ---
+--- Example
+---```lua
+-----Set 
+
+ntinuously
 ---for a steady light.
---- 
---- ---
---- Example
----```lua
------Pulsating, yellow light above world origo
----local intensity = 3 + math.sin(GetTime())
----PointLight(Vec(0, 5, 0), 1, 1, 0, intensity)
----```
----@param pos table World space light position
----@param r number Red
----@param g number Green
----@param b number Blue
----@param intensity number Intensity. Default is 1.0.
-function PointLight(pos, r, g, b, intensity) end
-
----Experimental. Scale time in order to make a slow-motion effect. Audio will
----also be affected. Note that this will affect physics behavior and is not
----intended for gameplay purposes. Calling this function will slow down time
----for the next frame only. Call every frame from tick function to get steady
----slow-motion.
---- 
---- ---
---- Example
----```lua
------Slow down time when holding down a key
----if InputDown('t') then
----SetTimeScale(0.2)
----end
----```
----@param scale number Time scale 0.1 to 1.0
-function SetTimeScale(scale) end
-
----Reset the environment properties to default. This is often useful before 
----setting up a custom environment.
---- 
---- ---
---- Example
----```lua
----SetEnvironmentDefault()
----```
-function SetEnvironmentDefault() end
-
----This function is used for manipulating the environment properties. The available properties are 
----exactly the same as in the editor, except for "snowonground" which is not currently supported.
---- 
---- ---
---- Example
----```lua
----SetEnvironmentProperty("skybox", "cloudy.dds")
----SetEnvironmentProperty("rain", 0.7)
----SetEnvironmentProperty("fogcolor", 0.5, 0.5, 0.8)
----SetEnvironmentProperty("nightlight", false)
----```
----@param name string Property name
----@param value0 any Property value (type depends on property)
----@param value1 any Extra property value (only some properties)
----@param value2 any Extra property value (only some properties)
----@param value3 any Extra property value (only some properties)
-function SetEnvironmentProperty(name, value0, value1, value2, value3) end
-
----This function is used for querying the current environment properties. The available properties are
----exactly the same as in the editor.
---- 
---- ---
---- Example
----```lua
----local skyboxPath = GetEnvironmentProperty("skybox")
----local rainValue = GetEnvironmentProperty("rain")
----local r,g,b = GetEnvironmentProperty("fogcolor")
----local enabled = GetEnvironmentProperty("nightlight")
----```
----@param name string Property name
----@return any value0 Property value (type depends on property)
----@return any value1 Property value (only some properties)
----@return any value2 Property value (only some properties)
----@return any value3 Property value (only some properties)
----@return any value4 Property value (only some properties)
-function GetEnvironmentProperty(name) end
-
----Reset the post processing properties to default.
---- 
---- ---
---- Example
----```lua
----SetPostProcessingDefault()
----```
-function SetPostProcessingDefault() end
-
----This function is used for manipulating the post processing properties. The available properties are
----exactly the same as in the editor.
---- 
---- ---
---- Example
----```lua
------Sepia post processing
----SetPostProcessingProperty("saturation", 0.4)
----SetPostProcessingProperty("colorbalance", 1.3, 1.0, 0.7)
----```
----@param name string Property name
----@param value0 number Property value
----@param value1 number Extra property value (only some properties)
----@param value2 number Extra property value (only some properties)
-function SetPostProcessingProperty(name, value0, value1, value2) end
-
----This function is used for querying the current post processing properties. 
----The available properties are exactly the same as in the editor.
---- 
---- ---
---- Example
----```lua
----local saturation = GetPostProcessingProperty("saturation")
----local r,g,b = GetPostProcessingProperty("colorbalance")
----```
----@param name string Property name
----@return number value0 Property value
----@return number value1 Property value (only some properties)
----@return number value2 Property value (only some properties)
-function GetPostProcessingProperty(name) end
-
----Draw a 3D line. In contrast to DebugLine, it will not show behind objects. Default color is white.
---- 
---- ---
---- Example
----```lua
------Draw white debug line
----DrawLine(Vec(0, 0, 0), Vec(-10, 5, -10))
----
------Draw red debug line
----DrawLine(Vec(0, 0, 0), Vec(10, 5, 10), 1, 0, 0)
----```
----@param p0 table World space point as vector
----@param p1 table World space point as vector
----@param r number Red
----@param g number Green
----@param b number Blue
+
+ault is 1.0.
+function PointLight(pos, r, g,
+
+Scale(0.2)
+---end
+---```
+---@param scale number 
+
+tEnvironmentProperty("skybox", "
+
+rty name
+---@param value0 any Proper
+
+roperty name
+---@return any value0 Property value (type depends on proper
+
+nce", 1.3, 1.0, 0.7)
+---```
+---@param nam
+
+)
+---@param value2 number Extra propert
+
+ome properties)
+---@return number value2 Property value (only some p
+
+ue
 ---@param a number Alpha
-function DrawLine(p0, p1, r, g, b, a) end
-
----Draw a 3D debug overlay line in the world. Default color is white.
---- 
---- ---
---- Example
----```lua
------Draw white debug line
----DebugLine(Vec(0, 0, 0), Vec(-10, 5, -10))
----
------Draw red debug line
----DebugLine(Vec(0, 0, 0), Vec(10, 5, 10), 1, 0, 0)
----```
----@param p0 table World space point as vector
----@param p1 table World space point as vector
----@param r number Red
----@param g number Green
----@param b number Blue
----@param a number Alpha
-function DebugLine(p0, p1, r, g, b, a) end
-
----Draw a debug cross in the world to highlight a location. Default color is white.
---- 
---- ---
---- Example
----```lua
----DebugCross(Vec(10, 5, 5))
----```
----@param p0 table World space point as vector
----@param r number Red
----@param g number Green
----@param b number Blue
----@param a number Alpha
-function DebugCross(p0, r, g, b, a) end
-
----Show a named valued on screen for debug purposes.
----Up to 32 values can be shown simultaneously. Values updated the current
----frame are drawn opaque. Old values are drawn transparent in white.
----The function will also recognize vectors, quaternions and transforms as
----second argument and convert them to strings automatically.
---- 
---- ---
---- Example
----```lua
----local t = 5
----DebugWatch("time", t)
----```
----@param name string Name
----@param value string Value
-function DebugWatch(name, value) end
-
----Display message on screen. The last 20 lines are displayed.
---- 
---- ---
---- Example
----```lua
----DebugPrint("time")
----```
----@param message string Message to display
-function DebugPrint(message) end
-
----Calling this function will disable game input, bring up the mouse pointer
----and allow Ui interaction with the calling script without pausing the game.
----This can be useful to make interactive user interfaces from scripts while
----the game is running. Call this continuously every frame as long as Ui 
----interaction is desired.
---- 
---- ---
---- Example
----```lua
----UiMakeInteractive()
----```
-function UiMakeInteractive() end
-
----Push state onto stack. This is used in combination with UiPop to
----remember a state and restore to that state later.
---- 
---- ---
---- Example
----```lua
+function DrawLin
+
+n DebugLine(p0, p1, r, g, b, a) end
+
+---D
+
+ent
+---frame are drawn opaque. Old values 
+
+lue
+function DebugWatch(name, value) en
+
+tinuously every frame as long as Ui 
+
+ation with UiPop to
+---remember 
+
+``lua
 ---UiColor(1,0,0)
----UiText("Red")
----UiPush()
----	UiColor(0,1,0)
----	UiText("Green")
----UiPop()
----UiText("Red")
----```
-function UiPush() end
-
----Pop state from stack and make it the current one. This is used in
----combination with UiPush to remember a previous state and go back to
----it later.
---- 
---- ---
---- Example
----```lua
----UiColor(1,0,0)
----UiText("Red")
----UiPush()
----	UiColor(0,1,0)
----	UiText("Green")
----UiPop()
----UiText("Red")
----```
-function UiPop() end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local w = UiWidth()
----```
----@return number width Width of draw context
-function UiWidth() end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local h = UiHeight()
----```
----@return number height Height of draw context
-function UiHeight() end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local c = UiCenter()
------Same as 
----local c = UiWidth()/2
----```
----@return number center Half width of draw context
-function UiCenter() end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local m = UiMiddle()
------Same as
----local m = UiHeight()/2
----```
----@return number middle Half height of draw context
-function UiMiddle() end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Set color yellow
----UiColor(1,1,0)
----```
----@param r number Red channel
----@param g number Green channel
----@param b number Blue channel
----@param a number Alpha channel. Default 1.0
-function UiColor(r, g, b, a) end
-
----Color filter, multiplied to all future colors in this scope
---- 
---- ---
---- Example
----```lua
----UiPush()
----	--Draw menu in transparent, yellow color tint
----	UiColorFilter(1, 1, 0, 0.5)
----	drawMenu()
----UiPop()
----```
----@param r number Red channel
----@param g number Green channel
----@param b number Blue channel
----@param a number Alpha channel. Default 1.0
-function UiColorFilter(r, g, b, a) end
-
----Translate cursor
---- 
---- ---
---- Example
----```lua
----UiPush()
----	UiTranslate(100, 0)
+---UiTex
+
+iption
+--- 
+--- ---
+-
+
+nter() end
+
+---No De
+
+middle Half height of 
+
+`
+---@param r number Re
+
+ied to all future color
+
+-@param r number Red ch
+
+)
 ---	UiText("Indented")
----UiPop()
----```
----@param x number X component
----@param y number Y component
-function UiTranslate(x, y) end
-
----Rotate cursor
---- 
---- ---
---- Example
----```lua
----UiPush()
----	UiRotate(45)
----	UiText("Rotated")
----UiPop()
----```
----@param angle number Angle in degrees, counter clockwise
-function UiRotate(angle) end
-
----Scale cursor either uniformly (one argument) or non-uniformly (two arguments)
---- 
---- ---
---- Example
----```lua
----UiPush()
----	UiScale(2)
----	UiText("Double size")
----UiPop()
----```
----@param x number X component
----@param y number Y component. Default value is x.
-function UiScale(x, y) end
-
----Set up new bounds. Calls to UiWidth, UiHeight, UiCenter and UiMiddle
----will operate in the context of the window size. 
----If clip is set to true, contents of window will be clipped to 
----bounds (only works properly for non-rotated windows).
---- 
---- ---
---- Example
----```lua
----UiPush()
----	UiWindow(400, 200)
----	local w = UiWidth()
----	--w is now 400
----UiPop()
----```
----@param width number Window width
----@param height number Window height
----@param clip boolean Clip content outside window. Default is false.
-function UiWindow(width, height, clip) end
-
----Return a safe drawing area that will always be visible regardless of
----display aspect ratio. The safe drawing area will always be 1920 by 1080
----in size. This is useful for setting up a fixed size UI.
---- 
---- ---
---- Example
----```lua
----function draw()
----	local x0, y0, x1, y1 = UiSafeMargins()
----	UiTranslate(x0, y0)
----	UiWindow(x1-x0, y1-y0, true)
----	--The drawing area is now 1920 by 1080 in the center of screen
----	drawMenu()
----end
----```
----@return number x0 Left
----@return number y0 Top
+---UiPo
+
+niformly (two arguments)
+--- 
+--- ---
+
+ end
+
+---Set up new bounds. Ca
+
+rks properly for non-rotated
+
+t is false.
+function UiWin
+
+ber y0 Top
 ---@return number x1 Right
----@return number y1 Bottom
-function UiSafeMargins() end
-
----The alignment determines how content is aligned with respect to the
----cursor.
----
----Alignment  Description
----left	 Horizontally align to the leftright	 Horizontally align to the rightcenter	 Horizontally align to the centertop		 Vertically align to the topbottom	 Veritcally align to the bottommiddle	 Vertically align to the middle
---- 
---- ---
---- Example
----```lua
----UiAlign("left")
----UiText("Aligned left at baseline")
----
----UiAlign("center middle")
----UiText("Fully centered")
----```
----@param alignment string Alignment keywords
-function UiAlign(alignment) end
-
----Disable input for everything, except what's between UiModalBegin and UiModalEnd 
----(or if modal state is popped)
---- 
---- ---
---- Example
----```lua
----UiModalBegin()
----if UiTextButton("Okay") then
----	--All other interactive ui elements except this one are disabled
----end
----UiModalEnd()
----
------This is also okay
----UiPush()
----	UiModalBegin()
----	if UiTextButton("Okay") then
----		--All other interactive ui elements except this one are disabled
----	end
----UiPop()
------No longer modal
----```
-function UiModalBegin() end
-
----Disable input for everything, except what's between UiModalBegin and UiModalEnd
----Calling this function is optional. Modality is part of the current state and will
----be lost if modal state is popped.
---- 
---- ---
---- Example
----```lua
----UiModalBegin()
----if UiTextButton("Okay") then
----	--All other interactive ui elements except this one are disabled
----end
----UiModalEnd()
----```
-function UiModalEnd() end
-
----Disable input
---- 
---- ---
---- Example
----```lua
----UiPush()
----	UiDisableInput()
----	if UiTextButton("Okay") then
----		--Will never happen
----	end
----UiPop()
----```
-function UiDisableInput() end
-
----Enable input that has been previously disabled
---- 
---- ---
---- Example
----```lua
----UiDisableInput()
----if UiTextButton("Okay") then
----	--Will never happen
----end
----
----UiEnableInput()
----if UiTextButton("Okay") then
----	--This can happen
----end
----```
-function UiEnableInput() end
-
----This function will check current state receives input. This is the case 
----if input is not explicitly disabled with (with UiDisableInput) and no other
----state is currently modal (with UiModalBegin). Input functions and UI
----elements already do this check internally, but it can sometimes be useful 
----to read the input state manually to trigger things in the UI.
---- 
---- ---
---- Example
----```lua
----if UiReceivesInput() then
----	highlightItemAtMousePointer()
----end
----```
----@return boolean receives True if current context receives input
-function UiReceivesInput() end
-
----Get mouse pointer position relative to the cursor
---- 
---- ---
---- Example
----```lua
----local x, y = UiGetMousePos()
----```
----@return number x X coordinate
----@return number y Y coordinate
-function UiGetMousePos() end
-
----Check if mouse pointer is within rectangle. Note that this function respects
----alignment.
---- 
---- ---
---- Example
----```lua
----if UiIsMouseInRect(100, 100) then
----	-- mouse pointer is in rectangle
----end
----```
----@param w number Width
----@param h number Height
----@return boolean inside True if mouse pointer is within rectangle
-function UiIsMouseInRect(w, h) end
-
----Convert world space position to user interface X and Y coordinate relative
----to the cursor. The distance is in meters and positive if in front of camera,
+---@
+
+nment string Alignment keywo
+
+ModalBegin() end
+
+---Disable in
+
+n("Okay") then
+---		--Will 
+
+t state receives input. T
+
+ements already do this check 
+
+t context receives input
+fun
+
+ mouse pointer is within recta
+
+,
 ---negative otherwise.
---- 
---- ---
---- Example
----```lua
----local x, y, dist = UiWorldToPixel(point)
----if dist > 0 then
----UiTranslate(x, y)
----UiText("Label")
----end
----```
----@param point table 3D world position as vector
----@return number x X coordinate
----@return number y Y coordinate
----@return number distance Distance to point
-function UiWorldToPixel(point) end
-
----Convert X and Y UI coordinate to a world direction, as seen from current camera.
----This can be used to raycast into the scene from the mouse pointer position.
---- 
---- ---
---- Example
----```lua
----UiMakeInteractive()
----local x, y = UiGetMousePos()
----local dir = UiPixelToWorld(x, y)
----local pos = GetCameraTransform().pos
----local hit, dist = QueryRaycast(pos, dir, 100)
----if hit then
----	DebugPrint("hit distance: " .. dist)
----end
----```
----@param x number X coordinate
----@param y number Y coordinate
----@return table direction 3D world direction as vector
-function UiPixelToWorld(x, y) end
-
----Perform a gaussian blur on current screen content
---- 
---- ---
---- Example
----```lua
----UiBlur(1.0)
----drawMenu()
----```
----@param amount number Blur amount (0.0 to 1.0)
-function UiBlur(amount) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----UiFont("bold.ttf", 24)
----UiText("Hello")
----```
----@param path string Path to TTF font file
----@param size number Font size (10 to 100)
-function UiFont(path, size) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local h = UiFontHeight()
----```
----@return number size Font size
-function UiFontHeight() end
-
----No Description
---- 
---- ---
---- Example
----```lua
----UiFont("bold.ttf", 24)
----UiText("Hello")
----
----...
----
------Automatically advance cursor
----UiText("First line", true)
----UiText("Second line", true)
----```
----@param text string Print text at cursor location
----@param move boolean Automatically move cursor vertically. Default false.
----@return number w Width of text
----@return number h Height of text
-function UiText(text, move) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----local w, h = UiGetTextSize("Some text")
----```
----@param text string A text string
----@return number w Width of text
----@return number h Height of text
-function UiGetTextSize(text) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----UiWordWrap(200)
----UiText("Some really long text that will get wrapped into several lines")
----```
----@param width number Maximum width of text
-function UiWordWrap(width) end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Black outline, standard thickness
----UiTextOutline(0,0,0,1)
----UiText("Text with outline")
----```
----@param r number Red channel
----@param g number Green channel
----@param b number Blue channel
----@param a number Alpha channel
----@param thickness number Outline thickness. Default is 0.1
-function UiTextOutline(r, g, b, a, thickness) end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Black drop shadow, 50% transparent, distance 2
----UiTextShadow(0, 0, 0, 0.5, 2.0)
----UiText("Text with drop shadow")
----```
----@param r number Red channel
----@param g number Green channel
----@param b number Blue channel
----@param a number Alpha channel
----@param distance number Shadow distance. Default is 1.0
----@param blur number Shadow blur. Default is 0.5
-function UiTextShadow(r, g, b, a, distance, blur) end
-
----Draw solid rectangle at cursor position
---- 
---- ---
---- Example
----```lua
------Draw full-screen black rectangle
----UiColor(0, 0, 0)
----UiRect(UiWidth(), UiHeight())
----
------Draw smaller, red, rotating rectangle in center of screen
----UiPush()
----	UiColor(1, 0, 0)
----	UiTranslate(UiCenter(), UiMiddle())
----	UiRotate(GetTime())
----	UiAlign("center middle")
----	UiRect(100, 100)
----UiPop()
----```
----@param w number Width
----@param h number Height
-function UiRect(w, h) end
-
----Draw image at cursor position
---- 
---- ---
---- Example
----```lua
------Draw image in center of screen
----UiPush()
----	UiTranslate(UiCenter(), UiMiddle())
----	UiAlign("center middle")
----	UiImage("test.png")
----UiPop()
----```
----@param path string Path to image (PNG or JPG format)
----@return number w Image width
----@return number h Image height
-function UiImage(path) end
-
----Get image size
---- 
---- ---
---- Example
----```lua
----local w,h = UiGetImageSize("test.png")
----```
----@param path string Path to image (PNG or JPG format)
----@return number w Image width
----@return number h Image height
-function UiGetImageSize(path) end
-
----Draw 9-slice image at cursor position. Width should be at least 2*borderWidth.
----Height should be at least 2*borderHeight.
---- 
---- ---
---- Example
----```lua
----UiImageBox("menu-frame.png", 200, 200, 10, 10)
----```
----@param path string Path to image (PNG or JPG format)
----@param width number Width
----@param height number Height
----@param borderWidth number Border width
----@param borderHeight number Border height
-function UiImageBox(path, width, height, borderWidth, borderHeight) end
-
----UI sounds are not affected by acoustics simulation. Use LoadSound / PlaySound for that.
---- 
---- ---
---- Example
----```lua
----UiSound("click.ogg")
----```
----@param path string Path to sound file (OGG format)
----@param volume number Playback volume. Default 1.0
----@param pitch number Playback pitch. Default 1.0
----@param pan number Playback stereo panning (-1.0 to 1.0). Default 0.0.
-function UiSound(path, volume, pitch, pan) end
-
----Call this continuously to keep playing loop. 
----UI sounds are not affected by acoustics simulation. Use LoadLoop / PlayLoop for that.
---- 
---- ---
---- Example
----```lua
----if animating then
----	UiSoundLoop("screech.ogg")
----end
----```
----@param path string Path to looping sound file (OGG format)
----@param volume number Playback volume. Default 1.0
-function UiSoundLoop(path, volume) end
-
----Mute game audio and optionally music for the next frame. Call
----continuously to stay muted.
---- 
---- ---
---- Example
----```lua
----if menuOpen then
+---
+
+) end
+
+---Convert X and Y UI coord
+
+le direction 3D world direction as
+
+mber size Font size
+function UiFo
+
+st line", true)
+---UiText("
+
+rn number h Height of text
+func
+
+---```
+---@param text strin
+
+utline, standard thickness
+---U
+
+ber Outline thickness. Default i
+
+xt("Text with drop shadow")
+--
+
+--
+--- Example
+---```lua
+-----Draw full-screen bl
+
+--- Example
+---```lua
+-----Draw image in center of sc
+
+mage width
+---@return num
+
+Width
+---@param height num
+
+e LoadSound / PlaySound for that.
+
+by acoustics simulation. Use LoadLoop / PlayLoop for that.
+--- 
+--- ---
+
+en
 ---	UiMute(1.0)
 ---end
 ---```
----@param amount number Mute by this amount (0.0 to 1.0)
----@param music boolean Mute music as well
-function UiMute(amount, music) end
-
----Set up 9-slice image to be used as background for buttons.
---- 
---- ---
---- Example
----```lua
----UiButtonImageBox("button-9slice.png", 10, 10)
----if UiTextButton("Test") then
----	...
----end
----```
----@param path string Path to image (PNG or JPG format)
----@param borderWidth number Border width
----@param borderHeight number Border height
----@param r number Red multiply. Default 1.0
----@param g number Green multiply. Default 1.0
----@param b number Blue multiply. Default 1.0
----@param a number Alpha channel. Default 1.0
-function UiButtonImageBox(path, borderWidth, borderHeight, r, g, b, a) end
-
----Button color filter when hovering mouse pointer.
---- 
---- ---
---- Example
----```lua
----UiButtonHoverColor(1, 0, 0)
----if UiTextButton("Test") then
----	...
----end
----```
+---@param amo
+
+ (PNG or JPG format)
+---@param borderW
+
+borderWidth, borderHeight, r, g, b
+
+-```
 ---@param r number Red multiply
 ---@param g number Green multiply
----@param b number Blue multiply
----@param a number Alpha channel. Default 1.0
-function UiButtonHoverColor(r, g, b, a) end
-
----Button color filter when pressing down.
---- 
---- ---
---- Example
----```lua
----UiButtonPressColor(0, 1, 0)
----if UiTextButton("Test") then
----	...
----end
----```
----@param r number Red multiply
----@param g number Green multiply
----@param b number Blue multiply
----@param a number Alpha channel. Default 1.0
-function UiButtonPressColor(r, g, b, a) end
-
----The button offset when being pressed
---- 
---- ---
---- Example
----```lua
----UiButtonPressDistance(4)
----if UiTextButton("Test") then
----	...
----end
----```
----@param dist number Press distance
-function UiButtonPressDist(dist) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----if UiTextButton("Test") then
----	...
----end
----```
----@param text string Text on button
----@param w number Button width
----@param h number Button height
----@return boolean pressed True if user clicked button
-function UiTextButton(text, w, h) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----if UiImageButton("image.png") then
----	...
----end
----```
----@param path number Image path (PNG or JPG file)
----@return boolean pressed True if user clicked button
-function UiImageButton(path) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----if UiBlankButton(30, 30) then
----	...
----end
----```
----@param w number Button width
----@param h number Button height
----@return boolean pressed True if user clicked button
-function UiBlankButton(w, h) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----value = UiSlider("dot.png", "x", value, 0, 100)
----```
----@param path number Image path (PNG or JPG file)
----@param axis string Drag axis, must be "x" or "y"
----@param current number Current value
----@param min number Minimum value
----@param max number Maximum value
----@return number value New value, same as current if not changed
----@return boolean done True if user is finished changing (released slider)
-function UiSlider(path, axis, current, min, max) end
-
----No Description
---- 
---- ---
---- Example
----```lua
----name = UiTextInput(name, 200, 14)
----```
----@param text string Current text
----@param w number Width
----@param h number Height
----@param focus boolean (Focus?)
----@return string test Potentially altered text
-function UiTextInput(text, w, h, focus) end
-
----No Description
---- 
---- ---
---- Example
----```lua
------Turn off screen running current script
----screen = UiGetScreen()
----SetScreenEnabled(screen, false)
----```
----@return number handle Handle to the screen running this script or zero if none.
+---
+
+on UiButtonPressDist(dist) end
+
+---No Descr
+
+- 
+--- ---
+--- Example
+---```lua
+---if UiIm
+
+scription
+--- 
+--- ---
+--- Example
+-
+
+ua
+---value = UiSlider("dot.png", "x"
+
+aximum value
+---@return number v
+
+-name = UiTextInput(name, 200, 1
+
 function UiGetScreen() end
+

```

---

# Migration Report: tdext.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/tdext.lua
+++ patched/tdext.lua
@@ -1,31 +1,13 @@
----@param command string
+#version 2
 function Command(command, ...) end
 
----@param quat table
----@return string
 function QuatStr(quat) end
 
----@param transform table
----@return string
 function TransformStr(transform) end
 
----@param vector table
----@return string
 function VecStr(vector) end
 
----@param file string
----@return boolean
 function HasFile(file) end
 
-function init() end
+function handleCommand() end
 
----@param dt number
-function tick(dt) end
-
----@param dt number
-function update(dt) end
-
----@param dt number
-function draw(dt) end
-
-function handleCommand() end
```

---

# Migration Report: TDSU\tdsu.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/TDSU\tdsu.lua
+++ patched/TDSU\tdsu.lua
@@ -1,29 +1,4 @@
-#include "umf.lua"
-#include "util_color.lua"
-#include "util_debug.lua"
-#include "util_env.lua"
-#include "util_lua.lua"
-#include "util_math.lua"
-#include "util_quat.lua"
-#include "util_td.lua"
-#include "util_timer.lua"
-#include "util_tool.lua"
-#include "util_ui.lua"
-#include "util_umf.lua"
-#include "util_vec.lua"
-#include "util_vfx.lua"
-
-
---================================================================
---Teardown Scripting Utilities (TDSU)
---By: Cheejins
---================================================================
-
-
-_BOOLS = {} -- Control variable used for functions like CallOnce()
-
-
----INIT Initialize the utils library.
+#version 2
 function Init_Utils()
 
     InitDebug()
@@ -31,14 +6,13 @@
     InitTool(Tool)
     InitEnv()
 
-
     print("TDSU initialized.")
 
 end
 
----TICK Manage and run the utils library.
 function Tick_Utils()
 
     TickDebug(DB, db)
 
 end
+

```

---

# Migration Report: TDSU\umf.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/TDSU\umf.lua
+++ patched/TDSU\umf.lua
@@ -1,6710 +1,6 @@
--- UMF Framework by: Thomasims
+#version 2
+local __RUNLATER = {}
+local UMF_RUNLATER = function(code) __RUNLATER[#__RUNLATER + 1] = code end
+local __UMFLOADED = {["src/core/hook.lua"]=true,["src/util/detouring.lua"]=true,["src/core/hooks_base.lua"]=true,["src/core/hooks_extra.lua"]=true,["src/util/registry.lua"]=true,["src/util/debug.lua"]=true,["src/core/console_backend.lua"]=true,["src/core/_index.lua"]=true,["src/util/config.lua"]=true,["src/util/meta.lua"]=true,["src/util/constraint.lua"]=true,["src/util/resources.lua"]=true,["src/util/timer.lua"]=true,["src/util/visual.lua"]=true,["src/util/xml.lua"]=true,["src/vector/quat.lua"]=true,["src/vector/transform.lua"]=true,["src/vector/vector.lua"]=true,["src/entities/entity.lua"]=true,["src/entities/body.lua"]=true,["src/entities/joint.lua"]=true,["src/entities/light.lua"]=true,["src/entities/location.lua"]=true,["src/entities/player.lua"]=true,["src/entities/screen.lua"]=true,["src/entities/shape.lua"]=true,["src/entities/trigger.lua"]=true,["src/entities/vehicle.lua"]=true,["src/animation/animation.lua"]=true,["src/animation/armature.lua"]=true,["src/tool/tool.lua"]=true,["src/tdui/base.lua"]=true,["src/tdui/image.lua"]=true,["src/tdui/layout.lua"]=true,["src/tdui/panel.lua"]=true,["src/tdui/window.lua"]=true,["src/_index.lua"]=true,}
+local UMF_SOFTREQUIRE = function(name) return __UMFLOADED[name] end
 
-
-
--- UMF Package umf_complete_c v0.9.1 generated with:
--- build.lua -n "umf_complete_c v0.9.1" dist/umf_complete_c.lua src
---
-local __RUNLATER = {} local UMF_RUNLATER = function(code) __RUNLATER[#__RUNLATER + 1] = code end
-local __UMFLOADED = {["src/core/hook.lua"]=true,["src/util/detouring.lua"]=true,["src/core/hooks_base.lua"]=true,["src/core/hooks_extra.lua"]=true,["src/util/registry.lua"]=true,["src/util/debug.lua"]=true,["src/core/console_backend.lua"]=true,["src/core/_index.lua"]=true,["src/util/config.lua"]=true,["src/util/meta.lua"]=true,["src/util/constraint.lua"]=true,["src/util/resources.lua"]=true,["src/util/timer.lua"]=true,["src/util/visual.lua"]=true,["src/util/xml.lua"]=true,["src/vector/quat.lua"]=true,["src/vector/transform.lua"]=true,["src/vector/vector.lua"]=true,["src/entities/entity.lua"]=true,["src/entities/body.lua"]=true,["src/entities/joint.lua"]=true,["src/entities/light.lua"]=true,["src/entities/location.lua"]=true,["src/entities/player.lua"]=true,["src/entities/screen.lua"]=true,["src/entities/shape.lua"]=true,["src/entities/trigger.lua"]=true,["src/entities/vehicle.lua"]=true,["src/animation/animation.lua"]=true,["src/animation/armature.lua"]=true,["src/tool/tool.lua"]=true,["src/tdui/base.lua"]=true,["src/tdui/image.lua"]=true,["src/tdui/layout.lua"]=true,["src/tdui/panel.lua"]=true,["src/tdui/window.lua"]=true,["src/_index.lua"]=true,} local UMF_SOFTREQUIRE = function(name) return __UMFLOADED[name] end
---src/core/hook.lua
-(function() ----------------
--- Hook library
--- @script core.hook
-
-if hook then
-	return
-end
-
-local hook_table = {}
-local hook_compiled = {}
-
-local function recompile( event )
-	local hooks = {}
-	for k, v in pairs( hook_table[event] ) do
-		hooks[#hooks + 1] = v
-	end
-	hook_compiled[event] = hooks
-end
-
-hook = { table = hook_table }
-
---- Hooks a function to the specified event.
----
----@param event string
----@param identifier any
----@param func function
----@overload fun(event: string, func: function)
-function hook.add( event, identifier, func )
-	assert( type( event ) == "string", "Event must be a string" )
-	if func then
-		assert( identifier ~= nil, "Identifier must not be nil" )
-		assert( type( func ) == "function", "Callback must be a function" )
-	else
-		assert( type( identifier ) == "function", "Callback must be a function" )
-	end
-	hook_table[event] = hook_table[event] or {}
-	hook_table[event][identifier] = func or identifier
-	recompile( event )
-	return identifier
-end
-
---- Removes a hook to an event by its identifier.
----
----@param event string
----@param identifier any
-function hook.remove( event, identifier )
-	assert( type( event ) == "string", "Event must be a string" )
-	assert( identifier ~= nil, "Identifier must not be nil" )
-	if hook_table[event] then
-		hook_table[event][identifier] = nil
-		if next( hook_table[event] ) == nil then
-			hook_table[event] = nil
-			hook_compiled[event] = nil
-		else
-			recompile( event )
-		end
-	end
-end
-
---- Executes all hooks associated to an event.
----
----@param event string
----@return any
-function hook.run( event, ... )
-	local hooks = hook_compiled[event]
-	if not hooks then
-		return
-	end
-	for i = 1, #hooks do
-		local a, b, c, d, e = hooks[i]( ... )
-		if a ~= nil then
-			return a, b, c, d, e
-		end
-	end
-end
-
---- Executes all hooks associated to an event with `pcall`.
----
----@param event string
----@return any
-function hook.saferun( event, ... )
-	local hooks = hook_compiled[event]
-	if not hooks then
-		return
-	end
-	for i = 1, #hooks do
-		local s, a, b, c, d, e = softassert( pcall( hooks[i], ... ) )
-		if s and a ~= nil then
-			return a, b, c, d, e
-		end
-	end
-end
-
---- Tests if an event has hooks attached.
----
----@param event string
----@return boolean
-function hook.used( event )
-	return hook_table[event]
-end
-
-
- end)();
---src/util/detouring.lua
-(function() ----------------
--- Detour Utilities
--- @script util.detouring
-local original = {}
-local function call_original( name, ... )
-	local fn = original[name]
-	if fn then
-		return fn( ... )
-	end
-end
-
-local detoured = {}
---- Detours a global function even it gets reassigned afterwards.
----
----@param name string
----@param generator fun(original: function): function
-function DETOUR( name, generator )
-	original[name] = original[name] or rawget( _G, name )
-	detoured[name] = generator( function( ... )
-		return call_original( name, ... )
-	end )
-	rawset( _G, name, nil )
-end
-
-setmetatable( _G, {
-	__index = detoured,
-	__newindex = function( self, k, v )
-		if detoured[k] then
-			original[k] = v
-		else
-			rawset( self, k, v )
-		end
-	end,
-} )
-
- end)();
---src/core/hooks_base.lua
-(function() ----------------
--- Default hooks
--- @script core.hooks_base
-UMF_RUNLATER "UpdateQuickloadPatch()"
-
-local hook = hook
-
-local function checkoriginal( b, ... )
-	if not b then
-		printerror( ... )
-		return
-	end
-	return ...
-end
-
-local function simple_detour( name )
-	local event = "base." .. name
-	DETOUR( name, function( original )
-		return function( ... )
-			hook.saferun( event, ... )
-			return checkoriginal( pcall( original, ... ) )
-		end
-
-	end )
-end
-
-local detours = {
-	"init", -- "base.init" (runs before init())
-	"tick", -- "base.tick" (runs before tick())
-	"update", -- "base.update" (runs before update())
-}
-for i = 1, #detours do
-	simple_detour( detours[i] )
-end
-
---- Tests if a UI element should be drawn.
----
----@param kind string
----@return boolean
-function shoulddraw( kind )
-	return hook.saferun( "api.shoulddraw", kind ) ~= false
-end
-
-DETOUR( "draw", function( original )
-	return function( dt )
-		if shoulddraw( "all" ) then
-			hook.saferun( "base.predraw", dt )
-			if shoulddraw( "original" ) then
-				checkoriginal( pcall( original, dt ) )
-			end
-			hook.saferun( "base.draw", dt )
-		end
-	end
-
-end )
-
-DETOUR( "Command", function( original )
-	return function( cmd, ... )
-		hook.saferun( "base.precmd", cmd, { ... } )
-		local a, b, c, d, e, f = original( cmd, ... )
-		hook.saferun( "base.postcmd", cmd, { ... }, { a, b, c, d, e, f } )
-	end
-
-end )
-
------- QUICKSAVE WORKAROUND -----
--- Quicksaving stores a copy of the global table without functions, so libraries get corrupted on quickload
--- This code prevents this by overriding them back
-
-local saved = {}
-
-local function hasfunction( t, bck )
-	if bck[t] then
-		return
-	end
-	bck[t] = true
-	for k, v in pairs( t ) do
-		if type( v ) == "function" then
-			return true
-		end
-		if type( v ) == "table" and hasfunction( v, bck ) then
-			return true
-		end
-	end
-end
-
---- Updates the list of libraries known by the Quickload Patch.
-function UpdateQuickloadPatch()
-	for k, v in pairs( _G ) do
-		if k ~= "_G" and type( v ) == "table" and hasfunction( v, {} ) then
-			saved[k] = v
-		end
-	end
-end
-
-local quickloadfix = function()
-	for k, v in pairs( saved ) do
-		_G[k] = v
-	end
-end
-
-DETOUR( "handleCommand", function( original )
-	return function( command, ... )
-		if command == "quickload" then
-			quickloadfix()
-		end
-		hook.saferun( "base.command." .. command, ... )
-		return original( command, ... )
-	end
-end )
-
---------------------------------
-
-hook.add( "base.tick", "api.firsttick", function()
-	hook.remove( "base.tick", "api.firsttick" )
-	hook.saferun( "api.firsttick" )
-	if type( firsttick ) == "function" then
-		firsttick()
-	end
-end )
-
- end)();
---src/core/hooks_extra.lua
-(function() ----------------
--- @submodule core.hooks_base
-
---- Checks if the player is in a vehicle.
----
----@return boolean
-function IsPlayerInVehicle()
-	return GetBool( "game.player.usevehicle" )
-end
-
-local tool = GetString( "game.player.tool" )
-local invehicle = IsPlayerInVehicle()
-
-local keyboardkeys = { "esc", "up", "down", "left", "right", "space", "interact", "return" }
-for i = 97, 97 + 25 do
-	keyboardkeys[#keyboardkeys + 1] = string.char( i )
-end
-local function checkkeys( func, mousehook, keyhook )
-	if hook.used( keyhook ) and func( "any" ) then
-		for i = 1, #keyboardkeys do
-			if func( keyboardkeys[i] ) then
-				hook.saferun( keyhook, keyboardkeys[i] )
-			end
-		end
-	end
-	if hook.used( mousehook ) then
-		if func( "lmb" ) then
-			hook.saferun( mousehook, "lmb" )
-		end
-		if func( "rmb" ) then
-			hook.saferun( mousehook, "rmb" )
-		end
-	end
-end
-
-local mousekeys = { "lmb", "rmb", "mmb" }
-local heldkeys = {}
-
-hook.add( "base.tick", "api.default_hooks", function()
-	if InputLastPressedKey then
-		for i = 1, #mousekeys do
-			local k = mousekeys[i]
-			if InputPressed( k ) then
-				hook.saferun( "api.mouse.pressed", k )
-			elseif InputReleased( k ) then
-				hook.saferun( "api.mouse.released", k )
-			end
-		end
-		local lastkey = InputLastPressedKey()
-		if lastkey ~= "" then
-			heldkeys[lastkey] = true
-			hook.saferun( "api.key.pressed", lastkey )
-		end
-		for key in pairs( heldkeys ) do
-			if not InputDown( key ) then
-				heldkeys[key] = nil
-				hook.saferun( "api.key.released", key )
-				break
-			end
-		end
-		local wheel = InputValue( "mousewheel" )
-		if wheel ~= 0 then
-			hook.saferun( "api.mouse.wheel", wheel )
-		end
-		local mousedx = InputValue( "mousedx" )
-		local mousedy = InputValue( "mousedy" )
-		if mousedx ~= 0 or mousedy ~= 0 then
-			hook.saferun( "api.mouse.move", mousedx, mousedy )
-		end
-	elseif InputPressed then
-		checkkeys( InputPressed, "api.mouse.pressed", "api.key.pressed" )
-		checkkeys( InputReleased, "api.mouse.released", "api.key.released" )
-		local wheel = InputValue( "mousewheel" )
-		if wheel ~= 0 then
-			hook.saferun( "api.mouse.wheel", wheel )
-		end
-		local mousedx = InputValue( "mousedx" )
-		local mousedy = InputValue( "mousedy" )
-		if mousedx ~= 0 or mousedy ~= 0 then
-			hook.saferun( "api.mouse.move", mousedx, mousedy )
-		end
-	end
-
-	local n_invehicle = IsPlayerInVehicle()
-	if invehicle ~= n_invehicle then
-		hook.saferun( n_invehicle and "api.player.enter_vehicle" or "api.player.exit_vehicle",
-		              n_invehicle and GetPlayerVehicle() )
-		invehicle = n_invehicle
-	end
-
-	local n_tool = GetString( "game.player.tool" )
-	if tool ~= n_tool then
-		hook.saferun( "api.player.switch_tool", n_tool, tool )
-		tool = n_tool
-	end
-end )
-
- end)();
---src/util/registry.lua
-(function() ----------------
--- Registry Utilities
--- @script util.registry
-local coreloaded = UMF_SOFTREQUIRE "src/core/_index.lua"
-
-util = util or {}
-
-do
-	local serialize_any, serialize_table
-
-	serialize_table = function( val, bck )
-		if bck[val] then
-			return "nil"
-		end
-		bck[val] = true
-		local entries = {}
-		for k, v in pairs( val ) do
-			entries[#entries + 1] = string.format( "[%s] = %s", serialize_any( k, bck ), serialize_any( v, bck ) )
-		end
-		return string.format( "{%s}", table.concat( entries, "," ) )
-	end
-
-	serialize_any = function( val, bck )
-		local vtype = type( val )
-		if vtype == "table" then
-			return serialize_table( val, bck )
-		elseif vtype == "string" then
-			return string.format( "%q", val )
-		elseif vtype == "function" or vtype == "userdata" then
-			return string.format( "nil --[[%s]]", tostring( val ) )
-		else
-			return tostring( val )
-		end
-	end
-
-	--- Serializes something to a lua-like string.
-	---
-	---@vararg any
-	---@return string
-	function util.serialize( ... )
-		local result = {}
-		for i = 1, select( "#", ... ) do
-			result[i] = serialize_any( select( i, ... ), {} )
-		end
-		return table.concat( result, "," )
-	end
-end
-
---- Unserializes something from a lua-like string.
----
----@param dt string
----@return ...
-function util.unserialize( dt )
-	local fn = loadstring( "return " .. dt )
-	if fn then
-		setfenv( fn, {} )
-		return fn()
-	end
-end
-
-do
-	local function serialize_any( val, bck )
-		local vtype = type( val )
-		if vtype == "table" then
-			if bck[val] then
-				return "{}"
-			end
-			bck[val] = true
-			local len = 0
-			for k, v in pairs( val ) do
-				len = len + 1
-			end
-			local rt = {}
-			if len == #val then
-				for i = 1, #val do
-					rt[i] = serialize_any( val[i], bck )
-				end
-				return string.format( "[%s]", table.concat( rt, "," ) )
-			else
-				for k, v in pairs( val ) do
-					if type( k ) == "string" or type( k ) == "number" then
-						rt[#rt + 1] = string.format( "%s: %s", serialize_any( k, bck ), serialize_any( v, bck ) )
-					end
-				end
-				return string.format( "{%s}", table.concat( rt, "," ) )
-			end
-		elseif vtype == "string" then
-			return string.format( "%q", val )
-		elseif vtype == "function" or vtype == "userdata" or vtype == "nil" then
-			return "null"
-		else
-			return tostring( val )
-		end
-	end
-
-	--- Serializes something to a JSON string.
-	---
-	---@param val any
-	---@return string
-	function util.serializeJSON( val )
-		return serialize_any( val, {} )
-	end
-end
-
---- Creates a buffer shared via the registry.
----
----@param name string
----@param max? number
----@return table
-function util.shared_buffer( name, max )
-	max = max or 64
-	return {
-		_pos_name = name .. ".position",
-		_list_name = name .. ".list.",
-		push = function( self, text )
-			local cpos = GetInt( self._pos_name )
-			SetString( self._list_name .. (cpos % max), text )
-			SetInt( self._pos_name, cpos + 1 )
-		end,
-		len = function( self )
-			return math.min( GetInt( self._pos_name ), max )
-		end,
-		pos = function( self )
-			return GetInt( self._pos_name )
-		end,
-		get = function( self, index )
-			local pos = GetInt( self._pos_name )
-			local len = math.min( pos, max )
-			if index >= len then
-				return
-			end
-			return GetString( self._list_name .. (pos + index - len) % max )
-		end,
-		iterator = function( self )
-			local pos = GetInt( self._pos_name )
-			local len = math.min( pos, max )
-			return function( _, i )
-				i = (i or 0) + 1
-				if i >= len then
-					return
-				end
-				return i, GetString( self._list_name .. (pos + i - len) % max )
-			end
-		end,
-		get_g = function( self, index )
-			return GetString( self._list_name .. (index % max) )
-		end,
-		clear = function( self )
-			SetInt( self._pos_name, 0 )
-			ClearKey( self._list_name:sub( 1, -2 ) )
-		end,
-	}
-end
-
-if coreloaded then
-	--- Creates a channel shared via the registry.
-	---
-	---@param name string Name of the channel.
-	---@param max? number Maximum amount of unread messages in the channel.
-	---@param local_realm? string Name to use to identify the local recipient.
-	---@return table
-	function util.shared_channel( name, max, local_realm )
-		max = max or 64
-		local channel = {
-			_buffer = util.shared_buffer( name, max ),
-			_offset = 0,
-			_hooks = {},
-			_ready_count = 0,
-			_ready = {},
-			broadcast = function( self, ... )
-				return self:send( "", ... )
-			end,
-			send = function( self, realm, ... )
-				self._buffer:push( string.format( ",%s,;%s",
-				                                  (type( realm ) == "table" and table.concat( realm, "," ) or tostring( realm )),
-				                                  util.serialize( ... ) ) )
-			end,
-			listen = function( self, callback )
-				if self._ready[callback] ~= nil then
-					return
-				end
-				self._hooks[#self._hooks + 1] = callback
-				self:ready( callback )
-				return callback
-			end,
-			unlisten = function( self, callback )
-				self:unready( callback )
-				self._ready[callback] = nil
-				for i = 1, #self._hooks do
-					if self._hooks[i] == callback then
-						table.remove( self._hooks, i )
-						return true
-					end
-				end
-			end,
-			ready = function( self, callback )
-				if not self._ready[callback] then
-					self._ready_count = self._ready_count + 1
-					self._ready[callback] = true
-				end
-			end,
-			unready = function( self, callback )
-				if self._ready[callback] then
-					self._ready_count = self._ready_count - 1
-					self._ready[callback] = false
-				end
-			end,
-		}
-		local_realm = "," .. (local_realm or "unknown") .. ","
-		local function receive( ... )
-			for i = 1, #channel._hooks do
-				local f = channel._hooks[i]
-				if channel._ready[f] then
-					f( channel, ... )
-				end
-			end
-		end
-		hook.add( "base.tick", name, function( dt )
-			if channel._ready_count > 0 then
-				local last_pos = channel._buffer:pos()
-				if last_pos > channel._offset then
-					for i = math.max( channel._offset, last_pos - max ), last_pos - 1 do
-						local message = channel._buffer:get_g( i )
-						local start = message:find( ";", 1, true )
-						local realms = message:sub( 1, start - 1 )
-						if realms == ",," or realms:find( local_realm, 1, true ) then
-							receive( util.unserialize( message:sub( start + 1 ) ) )
-							if channel._ready_count <= 0 then
-								channel._offset = i + 1
-								return
-							end
-						end
-					end
-					channel._offset = last_pos
-				end
-			end
-		end )
-		return channel
-	end
-
-	--- Creates an async reader on a channel for coroutines.
-	---
-	---@param channel table Name of the channel.
-	---@return table
-	function util.async_channel( channel )
-		local listener = {
-			_channel = channel,
-			_waiter = nil,
-			read = function( self )
-				self._waiter = coroutine.running()
-				if not self._waiter then
-					error( "async_channel:read() can only be used in a coroutine" )
-				end
-				self._channel:ready( self._handler )
-				return coroutine.yield()
-			end,
-			close = function( self )
-				if self._handler then
-					self._channel:unlisten( self._handler )
-				end
-			end,
-		}
-		listener._handler = listener._channel:listen( function( _, ... )
-			if listener._waiter then
-				local co = listener._waiter
-				listener._waiter = nil
-				listener._channel:unready( listener._handler )
-				return coroutine.resume( co, ... )
-			end
-		end )
-		listener._channel:unready( listener._handler )
-		return listener
-	end
-end
-
-do
-
-	local gets, sets = {}, {}
-
-	--- Registers a type unserializer.
-	---
-	---@param type string
-	---@param callback fun(data: string): any
-	function util.register_unserializer( type, callback )
-		gets[type] = function( key )
-			return callback( GetString( key ) )
-		end
-	end
-
-	if coreloaded then
-		hook.add( "api.newmeta", "api.createunserializer", function( name, meta )
-			gets[name] = function( key )
-				return setmetatable( {}, meta ):__unserialize( GetString( key ) )
-			end
-			sets[name] = function( key, value )
-				return SetString( key, meta.__serialize( value ) )
-			end
-		end )
-	end
-
-	--- Creates a table shared via the registry.
-	---
-	---@param name string
-	---@param base? table
-	---@return table
-	function util.shared_table( name, base )
-		return setmetatable( base or {}, {
-			__index = function( self, k )
-				local key = tostring( k )
-				local vtype = GetString( string.format( "%s.%s.type", name, key ) )
-				if vtype == "" then
-					return
-				end
-				return gets[vtype]( string.format( "%s.%s.val", name, key ) )
-			end,
-			__newindex = function( self, k, v )
-				local vtype = type( v )
-				local handler = sets[vtype]
-				if not handler then
-					return
-				end
-				local key = tostring( k )
-				if vtype == "table" then
-					local meta = getmetatable( v )
-					if meta and meta.__serialize and meta.__type then
-						vtype = meta.__type
-						v = meta.__serialize( v )
-						handler = sets.string
-					end
-				end
-				SetString( string.format( "%s.%s.type", name, key ), vtype )
-				handler( string.format( "%s.%s.val", name, key ), v )
-			end,
-		} )
-	end
-
-	--- Creates a table shared via the registry with a structure.
-	---
-	---@param name string
-	---@param base table
-	---@return table
-	---@overload fun(name: string): fun(base: table): table
-	function util.structured_table( name, base )
-		local function generate( base )
-			local root = {}
-			local keys = {}
-			for k, v in pairs( base ) do
-				local key = name .. "." .. tostring( k )
-				if type( v ) == "table" then
-					if #v == 0 then
-						root[k] = util.structured_table( key, v )
-					else
-						keys[k] = { type = v[1], key = key, default = v[2] }
-					end
-				elseif type( v ) == "string" then
-					keys[k] = { type = v, key = key }
-				else
-					root[k] = v
-				end
-			end
-			return setmetatable( root, {
-				__index = function( self, k )
-					local entry = keys[k]
-					if entry and gets[entry.type] then
-						if HasKey( entry.key ) then
-							return gets[entry.type]( entry.key )
-						else
-							return entry.default
-						end
-					end
-				end,
-				__newindex = function( self, k, v )
-					local entry = keys[k]
-					if entry and sets[entry.type] then
-						return sets[entry.type]( entry.key, v )
-					end
-				end,
-			} )
-		end
-		if type( base ) == "table" then
-			return generate( base )
-		end
-		return generate
-	end
-
-	gets.number = GetFloat
-	gets.integer = GetInt
-	gets.boolean = GetBool
-	gets.string = GetString
-	gets.table = util.shared_table
-
-	sets.number = SetFloat
-	sets.integer = SetInt
-	sets.boolean = SetBool
-	sets.string = SetString
-	sets.table = function( key, val )
-		local tab = util.shared_table( key )
-		for k, v in pairs( val ) do
-			tab[k] = v
-		end
-	end
-
-end
-
- end)();
---src/util/debug.lua
-(function() ----------------
--- Debug Utilities
--- @script util.debug
-util = util or {}
-
---- Gets the current line of code.
----
----@param level number stack depth
----@return string
-function util.current_line( level )
-	level = (level or 0) + 3
-	local _, line = pcall( error, "-", level )
-	if line == "-" then
-		_, line = pcall( error, "-", level + 1 )
-		if line == "-" then
-			return
-		end
-		line = "[C]:?"
-	else
-		line = line:sub( 1, -4 )
-	end
-	return line
-end
-
---- Gets the current stacktrack.
----
----@param start number starting stack depth
----@return string
-function util.stacktrace( start )
-	start = (start or 0) + 3
-	local stack, last = {}, nil
-	for i = start, 32 do
-		local _, line = pcall( error, "-", i )
-		if line == "-" then
-			if last == "-" then
-				break
-			end
-		else
-			if last == "-" then
-				stack[#stack + 1] = "[C]:?"
-			end
-			stack[#stack + 1] = line:sub( 1, -4 )
-		end
-		last = line
-	end
-	return stack
-end
-
- end)();
---src/core/console_backend.lua
-(function() ----------------
--- Console related functions
--- @script core.console_backend
-
-local console_buffer = util.shared_buffer( "game.console", 128 )
-
--- Console backend --
-
-local function maketext( ... )
-	local text = ""
-	local len = select( "#", ... )
-	for i = 1, len do
-		local s = tostring( select( i, ... ) )
-		if i < len then
-			s = s .. string.rep( " ", 8 - #s % 8 )
-		end
-		text = text .. s
-	end
-	return text
-end
-
-_OLDPRINT = _OLDPRINT or print
---- Prints its arguments in the specified color to the console.
---- Also prints to the screen if global `PRINTTOSCREEN` is set to true.
----
----@param r number
----@param g number
----@param b number
-function printcolor( r, g, b, ... )
-	local text = maketext( ... )
-	console_buffer:push( string.format( "%f;%f;%f;%s", r, g, b, text ) )
-	-- TODO: Use color
-	if PRINTTOSCREEN then
-		DebugPrint( text )
-	end
-	return _OLDPRINT( ... )
-end
-
---- Prints its arguments to the console.
---- Also prints to the screen if global `PRINTTOSCREEN` is set to true.
-function print( ... )
-	printcolor( 1, 1, 1, ... )
-end
-
---- Prints its arguments to the console.
---- Also prints to the screen if global `PRINTTOSCREEN` is set to true.
-function printinfo( ... )
-	printcolor( 0, .6, 1, ... )
-end
-
---- Prints a warning and the current stacktrace to the console.
---- Also prints to the screen if global `PRINTTOSCREEN` is set to true.
----
----@param msg any
-function warning( msg )
-	printcolor( 1, .7, 0, "[WARNING] " .. tostring( msg ) .. "\n  " .. table.concat( util.stacktrace( 1 ), "\n  " ) )
-end
-
-printwarning = warning
-
---- Prints its arguments to the console.
---- Also prints to the screen if global `PRINTTOSCREEN` is set to true.
-function printerror( ... )
-	printcolor( 1, .2, 0, ... )
-end
-
---- Clears the UMF console buffer.
-function clearconsole()
-	console_buffer:clear()
-end
-
---- To be used with `pcall`, checks success value and prints the error if necessary.
----
----@param b boolean
----@return any
-function softassert( b, ... )
-	if not b then
-		printerror( ... )
-	end
-	return b, ...
-end
-
-function assert( b, msg, ... )
-	if not b then
-		local m = msg or "Assertion failed"
-		warning( m )
-		return error( m, ... )
-	end
-	return b, msg, ...
-end
-
-
- end)();
---src/core/_index.lua
-(function() 
-GLOBAL_CHANNEL = util.shared_channel( "game.umf_global_channel", 128 )
-
- end)();
---src/util/config.lua
-(function() ----------------
--- Config Library
--- @script util.config
-local registryloaded = UMF_SOFTREQUIRE "src/util/registry.lua"
-
-if registryloaded then
-	--- Creates a structured table for the mod config
-	---
-	---@param def table
-	function OptionsKeys( def )
-		return util.structured_table( "savegame.mod", def )
-	end
-end
-
-OptionsMenu = setmetatable( {}, {
-	__call = function( self, def )
-		def.title_size = def.title_size or 50
-		local f = OptionsMenu.Group( def )
-		draw = function()
-			UiTranslate( UiCenter(), 60 )
-			UiPush()
-			local fw, fh = f()
-			UiPop()
-			UiTranslate( 0, fh + 20 )
-			UiFont( "regular.ttf", 30 )
-			UiAlign( "center top" )
-			UiButtonImageBox( "ui/common/box-outline-6.png", 6, 6 )
-			if UiTextButton( "Close" ) then
-				Menu()
-			end
-		end
-		return f
-	end,
-} )
-
-----------------
--- Organizers --
-----------------
-
---- Groups multiple options together
----
----@param def table
-function OptionsMenu.Group( def )
-	local elements = {}
-	if def.title then
-		elements[#elements + 1] = OptionsMenu.Text( def.title, {
-			size = def.title_size or 40,
-			pad_bottom = def.title_pad or 15,
-			align = def.title_align or "center top",
-		} )
-	end
-	for i = 1, #def do
-		elements[#elements + 1] = def[i]
-	end
-	local condition = def.condition
-	return function()
-		if condition and not condition() then
-			return 0, 0
-		end
-		local mw, mh = 0, 0
-		for i = 1, #elements do
-			UiPush()
-			local w, h = elements[i]()
-			UiPop()
-			UiTranslate( 0, h )
-			mh = mh + h
-			mw = math.max( mw, w )
-		end
-		return mw, mh
-	end
-end
-
---- Text section
----
----@param text string
----@param options? table
-function OptionsMenu.Text( text, options )
-	options = options or {}
-	local size = options.size or 30
-	local align = options.align or "left top"
-	local offset = options.offset or (align:find( "left" ) and -400) or 0
-	local font = options.font or "regular.ttf"
-	local padt = options.pad_top or 0
-	local padb = options.pad_bottom or 5
-	local condition = options.condition
-	return function()
-		if condition and not condition() then
-			return 0, 0
-		end
-		UiTranslate( offset, padt )
-		UiFont( font, size )
-		UiAlign( align )
-		UiWordWrap( 800 )
-		local tw, th = UiText( text )
-		return tw, th + padt + padb
-	end
-end
-
---- Spacer
----
----@param space number Vertical space
----@param spacew? number Horizontal space
----@param condition? function Condition function to enable this spacer
-function OptionsMenu.Spacer( space, spacew, condition )
-	return function()
-		if condition and not condition() then
-			return 0, 0
-		end
-		return spacew or 0, space
-	end
-end
-
-----------------
----- Values ----
-----------------
-
-local function getvalue( id, def, func )
-	local key = "savegame.mod." .. id
-	if HasKey( key ) then
-		return (func or GetString)( key )
-	else
-		return def
-	end
-end
-
-local function setvalue( id, val, func )
-	local key = "savegame.mod." .. id
-	if val ~= nil then
-		(func or SetString)( key, val )
-	else
-		ClearKey( key )
-	end
-end
-
---- Keybind value
----
----@param def table
-function OptionsMenu.Keybind( def )
-	local text = def.name or def.id
-	local size = def.size or 30
-	local padt = def.pad_top or 0
-	local padb = def.pad_bottom or 5
-	local value = string.upper( getvalue( def.id, def.default ) or "" )
-	if value == "" then
-		value = "<none>"
-	end
-	local pressed = false
-	local condition = def.condition
-	return function()
-		if condition and not condition() then
-			return 0, 0
-		end
-		UiTranslate( -4, padt )
-		UiFont( "regular.ttf", size )
-		local fheight = UiFontHeight()
-		UiAlign( "right top" )
-		local lw, lh = UiText( text )
-		UiTranslate( 8, 0 )
-		UiAlign( "left top" )
-		UiColor( 1, 1, 0 )
-		local tempv = value
-		if pressed then
-			tempv = "<press a key>"
-			local k = InputLastPressedKey()
-			if k == "esc" then
-				pressed = false
-			elseif k ~= "" then
-				value = string.upper( k )
-				tempv = value
-				setvalue( def.id, k )
-				pressed = false
-			end
-		end
-		local rw, rh = UiGetTextSize( tempv )
-		if UiTextButton( tempv ) then
-			pressed = not pressed
-		end
-		UiTranslate( rw, 0 )
-		if value ~= "<none>" then
-			UiColor( 1, 0, 0 )
-			if UiTextButton( "x" ) then
-				value = "<none>"
-				setvalue( def.id, "" )
-			end
-			UiTranslate( size * 0.8, 0 )
-		end
-		if getvalue( def.id ) then
-			UiColor( 0.5, 0.8, 1 )
-			if UiTextButton( "Reset" ) then
-				value = def.default and string.upper( def.default ) or "<none>"
-				setvalue( def.id )
-			end
-		end
-		return lw + 8 + rw, fheight + padt + padb
-	end
-end
-
---- Slider value
----
----@param def table
-function OptionsMenu.Slider( def )
-	local text = def.name or def.id
-	local size = def.size or 30
-	local padt = def.pad_top or 0
-	local padb = def.pad_bottom or 5
-	local min = def.min or 0
-	local max = def.max or 100
-	local range = max - min
-	local value = getvalue( def.id, def.default, GetFloat )
-	local format = string.format( "%%.%df", math.max( 0, math.floor( math.log10( 1000 / range ) ) ) )
-	local step = def.step
-	local condition = def.condition
-	return function()
-		if condition and not condition() then
-			return 0, 0
-		end
-		UiTranslate( -4, padt )
-		UiFont( "regular.ttf", size )
-		local fheight = UiFontHeight()
-		UiAlign( "right top" )
-		local lw, lh = UiText( text )
-		UiTranslate( 16, lh / 2 )
-		UiAlign( "left middle" )
-		UiColor( 1, 1, 0.5 )
-		UiRect( 200, 2 )
-		UiTranslate( -8, 0 )
-		local prev = value
-		value = UiSlider( "ui/common/dot.png", "x", (value - min) * 200 / range, 0, 200 ) * range / 200 + min
-		if value ~= prev then
-			setvalue( def.id, value, SetFloat )
-			if step then
-				value = math.floor( value / step + 0.5 ) * step
-			end
-		end
-		UiTranslate( 216, 0 )
-		UiText( string.format( format, value ) )
-		return lw + 224, fheight + padt + padb
-	end
-end
-
---- Toggle value
----
----@param def table
-function OptionsMenu.Toggle( def )
-	local text = def.name or def.id
-	local size = def.size or 30
-	local padt = def.pad_top or 0
-	local padb = def.pad_bottom or 5
-	local value = getvalue( def.id, def.default, GetBool )
-	local condition = def.condition
-	return function()
-		if condition and not condition() then
-			return 0, 0
-		end
-		UiTranslate( -4, padt )
-		UiFont( "regular.ttf", size )
-		local fheight = UiFontHeight()
-		UiAlign( "right top" )
-		local lw, lh = UiText( text )
-		UiTranslate( 8, 0 )
-		UiAlign( "left top" )
-		UiColor( 1, 1, 0 )
-		if UiTextButton( value and "Enabled" or "Disabled" ) then
-			value = not value
-			setvalue( def.id, value, SetBool )
-		end
-		return lw + 100, fheight + padt + padb
-	end
-end
-
- end)();
---src/util/meta.lua
-(function() ----------------
--- Metatable Utilities
--- @script util.meta
-local coreloaded = UMF_SOFTREQUIRE "src/core/_index.lua"
-
-local registered_meta = {}
-local reverse_meta = {}
-
---- Defines a new metatable type.
----
----@param name string
----@param parent? string
----@return table
-function global_metatable( name, parent, usecomputed )
-	local meta = registered_meta[name]
-	if meta then
-		if not parent then
-			return meta
-		end
-	else
-		meta = {}
-		meta.__index = meta
-		meta.__type = name
-		registered_meta[name] = meta
-		reverse_meta[meta] = name
-		if coreloaded then
-			hook.saferun( "api.newmeta", name, meta )
-		end
-	end
-	local newindex = rawset
-	if usecomputed then
-		local computed = {}
-		meta._C = computed
-		meta.__index = function( self, k )
-			local c = computed[k]
-			if c then
-				return c( self )
-			end
-			return meta[k]
-		end
-		meta.__newindex = function( self, k, v )
-			local c = computed[k]
-			if c then
-				return c( self, v )
-			end
-			return newindex( self, k, v )
-		end
-	end
-	if parent then
-		local parent_meta = global_metatable( parent )
-		if parent_meta.__newindex then
-			newindex = parent_meta.__newindex
-			if not meta.__newindex then
-				meta.__newindex = newindex
-			end
-		end
-		setmetatable( meta, { __index = parent_meta.__index } )
-	end
-	return meta
-end
-
---- Gets an existing metatable.
----
----@param name string
----@return table?
-function find_global_metatable( name )
-	if not name then
-		return
-	end
-	if type( name ) == "table" then
-		return reverse_meta[name]
-	end
-	return registered_meta[name]
-end
-
-local function findmeta( src, found )
-	if found[src] then
-		return
-	end
-	found[src] = true
-	local res
-	for k, v in pairs( src ) do
-		if type( v ) == "table" then
-			local dt
-			local m = getmetatable( v )
-			if m then
-				local name = reverse_meta[m]
-				if name then
-					dt = {}
-					dt[1] = name
-				end
-			end
-			local sub = findmeta( v, found )
-			if sub then
-				dt = dt or {}
-				dt[2] = sub
-			end
-			if dt then
-				res = res or {}
-				res[k] = dt
-			end
-		end
-	end
-	return res
-end
-
-if coreloaded then
-	-- I hate this but without a pre-quicksave handler I see no other choice.
-	local previous = -2
-	hook.add( "base.tick", "api.metatables.save", function( ... )
-		if GetTime() - previous > 2 then
-			previous = GetTime()
-			_G.GLOBAL_META_SAVE = findmeta( _G, {} )
-		end
-	end )
-
-	local function restoremeta( dst, src )
-		for k, v in pairs( src ) do
-			local dv = dst[k]
-			if type( dv ) == "table" then
-				if v[1] then
-					setmetatable( dv, global_metatable( v[1] ) )
-				end
-				if v[2] then
-					restoremeta( dv, v[2] )
-				end
-			end
-		end
-	end
-
-	hook.add( "base.command.quickload", "api.metatables.restore", function( ... )
-		if GLOBAL_META_SAVE then
-			restoremeta( _G, GLOBAL_META_SAVE )
-		end
-	end )
-end
- end)();
---src/util/constraint.lua
-(function() ----------------
--- Constraint Utilities
--- @script util.constraint
-
-if not GetEntityHandle then
-	GetEntityHandle = function( handle )
-		return handle
-	end
-end
-
-constraint = {}
-_UMFConstraints = {}
-local solvers = {}
-
-function constraint.RunUpdate( dt )
-	local offset = 0
-	for i = 1, #_UMFConstraints do
-		local v = _UMFConstraints[i + offset]
-		if v.joint and IsJointBroken( v.joint ) then
-			table.remove( _UMFConstraints, i + offset )
-			offset = offset - 1
-		else
-			local result = { c = v }
-			for j = 1, #v.solvers do
-				local s = v.solvers[j]
-				solvers[s.type]( s, result )
-			end
-			if result.angvel then
-				local l = VecLength( result.angvel )
-				ConstrainAngularVelocity( v.parent, v.child, VecScale( result.angvel, 1 / l ), l * 10, 0, v.max_aimp )
-			end
-		end
-	end
-end
-
-local coreloaded = UMF_SOFTREQUIRE "src/core/_index.lua"
-if coreloaded then
-	hook.add( "base.update", "umf.constraint", constraint.RunUpdate )
-end
-
-local function find_index( t, v )
-	for i = 1, #t do
-		if t[i] == v then
-			return i
-		end
-	end
-end
-
-function constraint.Relative( val, body )
-	if type( val ) == "table" and val.handle or type( val ) == "number" then
-		body = val
-		val = nil
-	end
-	if type( val ) == "table" and val.body then
-		body = val.body
-		val = val.val
-	end
-	return { body = GetEntityHandle( body or 0 ), val = val }
-end
-
-local function resolve_point( relative_val )
-	return TransformToParentPoint( GetBodyTransform( relative_val.body ), relative_val.val )
-end
-
-local function resolve_axis( relative_val )
-	return TransformToParentVec( GetBodyTransform( relative_val.body ), relative_val.val )
-end
-
-local function resolve_orientation( relative_val )
-	return TransformToParentTransform( GetBodyTransform( relative_val.body ),
-	                                   Transform( Vec(), relative_val.val or Quat() ) )
-end
-
-local function resolve_transform( relative_val )
-	return TransformToParentTransform( GetBodyTransform( relative_val.body ), relative_val.val )
-end
-
-local constraint_meta = global_metatable( "constraint" )
-
-function constraint.New( parent, child, joint )
-	return setmetatable( {
-		parent = GetEntityHandle( parent ),
-		child = GetEntityHandle( child ),
-		joint = GetEntityHandle( joint ),
-		solvers = {},
-		tmp = {},
-		active = false,
-	}, constraint_meta )
-end
-
-function constraint_meta:Rebuild()
-	if not self.active then
-		return
-	end
-	local index = self.lastbuild and find_index( _UMFConstraints, self.lastbuild ) or (#_UMFConstraints + 1)
-	local c = {
-		parent = self.parent,
-		child = self.child,
-		joint = self.joint,
-		solvers = {},
-		max_aimp = self.max_aimp or math.huge,
-		max_vimp = self.max_vimp or math.huge,
-	}
-	for i = 1, #self.solvers do
-		c.solvers[i] = self.solvers[i]:Build() or { type = "none" }
-	end
-	self.lastbuild = c
-	_UMFConstraints[index] = c
-end
-
-function constraint_meta:Activate()
-	self.active = true
-	self:Rebuild()
-	return self
-end
-
-local colors = { { 1, 0, 0 }, { 0, 1, 0 }, { 0, 0, 1 }, { 0, 1, 1 }, { 1, 0, 1 }, { 1, 1, 0 }, { 1, 1, 1 } }
-function constraint_meta:DrawDebug( c )
-	c = c or GetBodyTransform( self.child ).pos
-	for i = 1, #self.solvers do
-		local col = colors[(i - 1) % #colors + 1]
-		self.solvers[i]:DrawDebug( c, col[1], col[2], col[3] )
-	end
-end
-
-function constraint_meta:LimitAngularVelocity( maxangvel )
-	if self.tmp.asolver then
-		self.tmp.asolver.max_avel = maxangvel
-	else
-		self.tmp.max_avel = maxangvel
-	end
-	return self
-end
-
-function constraint_meta:LimitAngularImpulse( maxangimpulse )
-	self.max_aimp = maxangimpulse
-	return self
-end
-
-function constraint_meta:LimitVelocity( maxvel )
-	if self.tmp.vsolver then
-		self.tmp.vsolver.max_vel = maxvel
-	else
-		self.tmp.max_vel = maxvel
-	end
-	return self
-end
-
-function constraint_meta:LimitImpulse( maximpulse )
-	self.max_vimp = maximpulse
-	return self
-end
-
---------------------------------
---         Solver Base        --
---------------------------------
-
-local solver_meta = global_metatable( "constraint_solver" )
-
-function solver_meta:Build()
-end
-function solver_meta:DrawDebug()
-end
-
-function solvers:none()
-end
-
---------------------------------
---    Rotation Axis Solvers   --
---------------------------------
-
-function constraint_meta:ConstrainRotationAxis( axis, body )
-	self.tmp.vsolver = nil
-	self.tmp.asolver = nil
-	self.tmp.axis = constraint.Relative( axis, body )
-	return self
-end
-
-local solver_ra_sphere_meta = global_metatable( "constraint_ra_sphere_solver", "constraint_solver" )
-
-function constraint_meta:OnSphere( quat, body )
-	local s = setmetatable( {}, solver_ra_sphere_meta )
-	s.axis = self.tmp.axis
-	s.quat = constraint.Relative( quat, body )
-	s.max_avel = self.tmp.max_avel
-	self.tmp.vsolver = nil
-	self.tmp.asolver = s
-	self.solvers[#self.solvers + 1] = s
-	return self
-end
-
-function constraint_meta:AboveLatitude( min )
-	self.tmp.asolver.min_lat = min
-	return self
-end
-
-function constraint_meta:BelowLatitude( max )
-	self.tmp.asolver.max_lat = max
-	return self
-end
-
-function constraint_meta:WithinLatitudes( min, max )
-	return self:AboveLatitude( min ):BelowLatitude( max )
-end
-
-function constraint_meta:WithinLongitudes( min, max )
-	self.tmp.asolver.min_lng = min
-	self.tmp.asolver.max_lng = max
-	return self
-end
-
-function solver_ra_sphere_meta:DrawDebug( c, r, g, b )
-	local tr = resolve_orientation( self.quat )
-	tr.pos = c
-	local axis = VecNormalize( resolve_axis( self.axis ) )
-
-	local start_lng = self.min_lng or 0
-	local len_lng = self.max_lng and (start_lng - self.max_lng) % 360
-	if self.min_lat then
-		visual.drawpolygon( TransformToParentTransform( tr, Transform( Vec( 0, math.sin( math.rad( self.min_lat ) ), 0 ) ) ),
-		                    math.cos( math.rad( self.min_lat ) ), -start_lng, 40, { arc = len_lng, r = r, g = g, b = b } )
-	end
-	if self.max_lat then
-		visual.drawpolygon( TransformToParentTransform( tr, Transform( Vec( 0, math.sin( math.rad( self.max_lat ) ), 0 ) ) ),
-		                    math.cos( math.rad( self.max_lat ) ), -start_lng, 40, { arc = len_lng, r = r, g = g, b = b } )
-	end
-	if self.min_lng then
-		local start_lat = self.min_lat or 360
-		local len_lat = start_lat - (self.max_lat or 0)
-		visual.drawpolygon( TransformToParentTransform( tr, Transform( Vec(), QuatEuler( 0, 180 - self.min_lng, 90 ) ) ), 1,
-		                    180 - start_lat, 20, { arc = len_lat, r = r, g = g, b = b } )
-		visual.drawpolygon( TransformToParentTransform( tr, Transform( Vec(), QuatEuler( 0, 180 - self.max_lng, 90 ) ) ), 1,
-		                    180 - start_lat, 20, { arc = len_lat, r = r, g = g, b = b } )
-	end
-
-	DrawLine( tr.pos, VecAdd( tr.pos, axis ), r, g, b )
-end
-
-function solver_ra_sphere_meta:Build()
-	local quat = constraint.Relative( self.quat )
-	local lng
-	if self.min_lng then
-		local mid = (self.max_lng + self.min_lng) / 2
-		if self.max_lng < self.min_lng then
-			mid = mid + 180
-		end
-		lng = math.acos( math.cos( math.rad( self.min_lng - mid ) ) )
-		quat.val = QuatRotateQuat( QuatAxisAngle( QuatRotateVec( quat.val or Quat(), Vec( 0, 1, 0 ) ), -mid ),
-		                           quat.val or Quat() )
-	end
-	local axis = constraint.Relative( self.axis )
-	axis.val = VecNormalize( axis.val )
-	return {
-		type = "ra_sphere",
-		axis = axis,
-		quat = quat,
-		lng = lng,
-		min_lat = self.min_lat and math.rad( self.min_lat ) or nil,
-		max_lat = self.max_lat and math.rad( self.max_lat ) or nil,
-		max_avel = self.max_avel,
-	}
-end
-
-function solvers:ra_sphere( result )
-	local axis = resolve_axis( self.axis )
-	local tr = resolve_orientation( self.quat )
-	local local_axis = TransformToLocalVec( tr, axis )
-	local resv
-	local lat = math.asin( local_axis[2] )
-	if self.min_lat and lat < self.min_lat then
-		local c = VecNormalize( VecCross( Vec( 0, -1, 0 ), local_axis ) )
-		resv = VecScale( c, lat - self.min_lat )
-	elseif self.max_lat and lat > self.max_lat then
-		local c = VecNormalize( VecCross( Vec( 0, -1, 0 ), local_axis ) )
-		resv = VecScale( c, lat - self.max_lat )
-	end
-	if self.lng then
-		local l = math.sqrt( local_axis[1] ^ 2 + local_axis[3] ^ 2 )
-		if l > 0.05 then
-			local n = math.acos( local_axis[3] / l ) - self.lng
-			if n < 0 then
-				local c = VecNormalize( VecCross( VecCross( Vec( 0, 1, 0 ), local_axis ), local_axis ) )
-				resv = VecAdd( resv, VecScale( c, local_axis[1] > 0 and -n or n ) )
-				-- local c = VecNormalize( VecCross( Vec( 0, 0, -1 ), local_axis ) )
-				-- resv = VecAdd( resv, VecScale( c, -n ) )
-			end
-		end
-	end
-	if resv then
-		if self.max_avel then
-			local len = VecLength( resv )
-			if len > self.max_avel then
-				resv = VecScale( resv, self.max_avel / len )
-			end
-		end
-		result.angvel = VecAdd( result.angvel, TransformToParentVec( tr, resv ) )
-	end
-end
-
---------------------------------
---     Orientation Solvers    --
---------------------------------
-
-function constraint_meta:ConstrainOrientation( quat, body )
-	self.tmp.vsolver = nil
-	self.tmp.asolver = nil
-	self.tmp.quat = constraint.Relative( quat, body )
-	return self
-end
-
-local solver_quat_quat_meta = global_metatable( "constraint_quat_quat_solver", "constraint_solver" )
-
-function constraint_meta:ToOrientation( quat, body )
-	local s = setmetatable( {}, solver_quat_quat_meta )
-	s.quat1 = self.tmp.quat
-	s.quat2 = constraint.Relative( quat, body )
-	s.max_avel = self.tmp.max_avel
-	self.tmp.vsolver = nil
-	self.tmp.asolver = s
-	self.solvers[#self.solvers + 1] = s
-	return self
-end
-
-local cdirections = { Vec( 1, 0, 0 ), Vec( 0, 1, 0 ), Vec( 0, 0, 1 ) }
-function solver_quat_quat_meta:DrawDebug( c, r, g, b )
-	local tr1 = resolve_orientation( self.quat1 )
-	tr1.pos = c
-	local tr2 = resolve_orientation( self.quat2 )
-	tr2.pos = c
-	for i = 1, #cdirections do
-		local dir = cdirections[i]
-		local p1 = TransformToParentPoint( tr1, dir )
-		local p2 = TransformToParentPoint( tr2, dir )
-		DrawLine( tr1.pos, p1, r, g, b )
-		DrawLine( tr1.pos, p2, r, g, b )
-		DrawLine( p1, p2, r, g, b )
-	end
-end
-
-function solver_quat_quat_meta:Build()
-	return { type = "quat_quat", quat1 = self.quat1, quat2 = self.quat2, max_avel = self.max_avel or math.huge }
-end
-
-function solvers:quat_quat( result )
-	ConstrainOrientation( result.c.child, result.c.parent, resolve_orientation( self.quat1 ).rot,
-	                      resolve_orientation( self.quat2 ).rot, self.max_avel, result.c.max_aimp )
-end
-
---------------------------------
---      Position Solvers      --
---------------------------------
-
-function constraint_meta:ConstrainPoint( point, body )
-	self.tmp.vsolver = nil
-	self.tmp.asolver = nil
-	self.tmp.point = constraint.Relative( point, body )
-	return self
-end
-
-local solver_point_point_meta = global_metatable( "constraint_point_point_solver", "constraint_solver" )
-
-function constraint_meta:ToPoint( point, body )
-	local s = setmetatable( {}, solver_point_point_meta )
-	s.point1 = self.tmp.point
-	s.point2 = constraint.Relative( point, body )
-	s.max_vel = self.tmp.max_vel
-	self.tmp.vsolver = s
-	self.tmp.asolver = nil
-	self.solvers[#self.solvers + 1] = s
-	return self
-end
-
-function solver_point_point_meta:DrawDebug( c, r, g, b )
-	local point1 = resolve_point( self.point1 )
-	local point2 = resolve_point( self.point2 )
-	DebugCross( point1, r, g, b )
-	DebugCross( point2, r, g, b )
-	DrawLine( point1, point2, r, g, b )
-end
-
-function solver_point_point_meta:Build()
-	return { type = "point_point", point1 = self.point1, point2 = self.point2, max_vel = self.max_vel or math.huge }
-end
-
-function solvers:point_point( result )
-	ConstrainPosition( result.c.child, result.c.parent, resolve_point( self.point1 ), resolve_point( self.point2 ),
-	                   self.max_vel, result.c.max_vimp )
-end
-
-local solver_point_space_meta = global_metatable( "constraint_point_space_solver", "constraint_solver" )
-
-function constraint_meta:ToSpace( transform, body )
-	local s = setmetatable( {}, solver_point_space_meta )
-	s.point = self.tmp.point
-	s.transform = constraint.Relative( transform, body )
-	s.max_vel = self.tmp.max_vel
-	s.constraints = {}
-	self.tmp.vsolver = s
-	self.tmp.asolver = nil
-	self.solvers[#self.solvers + 1] = s
-	return self
-end
-
-function constraint_meta:WithinBox( center, min, max )
-	local rcenter = constraint.Relative( self.tmp.vsolver.transform )
-	rcenter.val = TransformToParentTransform( rcenter.val, center )
-	table.insert( self.tmp.vsolver.constraints, { type = "box", center = rcenter, min = min, max = max } )
-	return self
-end
-
-function constraint_meta:WithinSphere( center, radius )
-	local rcenter = constraint.Relative( self.tmp.vsolver.transform )
-	rcenter.val = TransformToParentPoint( rcenter.val, center )
-	table.insert( self.tmp.vsolver.constraints, { type = "sphere", center = rcenter, radius = radius } )
-	return self
-end
-
-function constraint_meta:AbovePlane( transform )
-	local rcenter = constraint.Relative( self.tmp.vsolver.transform )
-	rcenter.val = TransformToParentTransform( rcenter.val, transform )
-	table.insert( self.tmp.vsolver.constraints, { type = "plane", center = rcenter } )
-	return self
-end
-
-function solver_point_space_meta:DrawDebug( c, r, g, b )
-	local point = resolve_point( self.point )
-	for i = 1, #self.constraints do
-		local c = self.constraints[i]
-		if c.type == "plane" then
-			local tr = resolve_transform( c.center )
-			local lp = TransformToLocalPoint( tr, point )
-			lp[2] = 0
-			tr.pos = TransformToParentPoint( tr, lp )
-			visual.drawpolygon( tr, 1.414, 45, 4, { r = r, g = g, b = b } )
-		elseif c.type == "box" then
-			local tr = resolve_transform( c.center )
-			visual.drawbox( tr, c.min, c.max, { r = r, g = g, b = b } )
-		elseif c.type == "sphere" then
-			local tr = Transform( resolve_point( c.center ), Quat() )
-			visual.drawwiresphere( tr, c.radius, 32, { r = r, g = g, b = b } )
-		end
-	end
-end
-
-function solver_point_space_meta:Build()
-	local consts = {}
-	for i = 1, #self.constraints do
-		local c = self.constraints[i]
-		if c.type == "box" then
-			local rcenter = constraint.Relative( c.center )
-			rcenter.val.pos = TransformToParentPoint( rcenter.val, VecScale( VecAdd( c.min, c.max ), 0.5 ) )
-			consts[i] = { type = "box", center = rcenter, size = VecScale( VecSub( c.max, c.min ), 0.5 ) }
-		else
-			consts[i] = c
-		end
-	end
-	return { type = "point_space", point = self.point, constraints = consts, max_vel = self.max_vel or math.huge }
-end
-
-function solvers:point_space( result )
-	local point = resolve_point( self.point )
-	local resv
-	for i = 1, #self.constraints do
-		local c = self.constraints[i]
-		if c.type == "plane" then
-			local tr = resolve_transform( c.center )
-			local lp = TransformToLocalPoint( tr, point )
-			if lp[2] < 0 then
-				resv = VecAdd( resv, TransformToParentVec( tr, Vec( 0, lp[2], 0 ) ) )
-			end
-		elseif c.type == "box" then
-			local tr = resolve_transform( c.center )
-			local lp = TransformToLocalPoint( tr, point )
-			local sx, sy, sz = c.size[1], c.size[2], c.size[3]
-			local nlp = Vec( lp[1] < -sx and lp[1] + sx or lp[1] > sx and lp[1] - sx or 0,
-			                 lp[2] < -sy and lp[2] + sy or lp[2] > sy and lp[2] - sy or 0,
-			                 lp[3] < -sz and lp[3] + sz or lp[3] > sz and lp[3] - sz or 0 )
-			if nlp[1] ~= 0 or nlp[2] ~= 0 or nlp[3] ~= 0 then
-				resv = VecAdd( resv, TransformToParentVec( tr, nlp ) )
-			end
-		elseif c.type == "sphere" then
-			local center = resolve_point( c.center )
-			local diff = VecSub( point, center )
-			local len = VecLength( diff )
-			if len > c.radius then
-				resv = VecAdd( resv, VecScale( diff, (len - c.radius) / len ) )
-			end
-		end
-	end
-	if resv then
-		local len = VecLength( resv )
-		resv = VecScale( resv, 1 / len )
-		if self.max_vel and len > self.max_vel then
-			len = self.max_vel
-		end
-		ConstrainVelocity( result.c.parent, result.c.child, point, resv, len * 10, 0, result.c.max_vimp )
-	end
-end
-
- end)();
---src/util/resources.lua
-(function() ----------------
--- Resources Utilities
--- @script util.resources
-
-util = util or {}
-
-local mod
-do
-	local stack = util.stacktrace()
-	local function findmods( file )
-		local matches = {}
-		while file and #file > 0 do
-			matches[#matches + 1] = file
-			file = file:match( "^(.-)/[^/]*$" )
-		end
-
-		local found
-		for _, key in ipairs( ListKeys( "mods.available" ) ) do
-			local path = GetString( "mods.available." .. key .. ".path" )
-			for _, subpath in ipairs( matches ) do
-				if path:sub( -#subpath ) == subpath then
-					if found then
-						return
-					end
-					found = key
-					break
-				end
-			end
-		end
-		return found
-	end
-	for i = 1, #stack do
-		if stack[i] ~= "[C]:?" then
-			local t = stack[i]:match( "%[string \"%.%.%.(.*)\"%]:%d+" ) or stack[i]:match( "%.%.%.(.*):%d+" )
-			if t then
-				local found = findmods( t )
-				if found then
-					mod = found
-					MOD = found
-					break
-				end
-			end
-		end
-	end
-end
-
---- Resolves a given mod path to an absolute path.
----
----@param path string
----@return string path Absolute path
-function util.resolve_path( path )
-	-- TODO: support relative paths (relative to the current file)
-	-- TODO: return multiple matches if applicable
-	local replaced, n = path:gsub( "^MOD/", GetString( "mods.available." .. mod .. ".path" ) .. "/" )
-	if n == 0 then
-		replaced, n = path:gsub( "^LEVEL/", GetString( "game.levelpath" ):sub( 1, -5 ) .. "/" )
-	end
-	if n == 0 then
-		replaced, n = path:gsub( "^MODS/([^/]+)", function( mod )
-			return GetString( "mods.available." .. mod .. ".path" )
-		end )
-	end
-	if n == 0 then
-		return path
-	end
-	return replaced
-end
-
---- Load a lua file from its mod path.
----
----@param path string
----@return function
----@return string error_message
-function util.load_lua_resource( path )
-	return loadfile( util.resolve_path( path ) )
-end
-
- end)();
---src/util/timer.lua
-(function() ----------------
--- Timer Utilities
---
---              WARNING
---   Timers are reset on quickload!
--- Keep this in mind if you use them.
---
--- @script util.timer
-
-timer = {}
-timer._backlog = {}
-
-local backlog = timer._backlog
-
-local function sortedinsert( tab, val )
-	for i = #tab, 1, -1 do
-		if val.time < tab[i].time then
-			tab[i + 1] = val
-			return
-		end
-		tab[i + 1] = tab[i]
-	end
-	tab[1] = val
-end
-
-local diff = GetTime() -- In certain realms, GetTime() is not 0 right away
-
---- Creates a simple timer to execute code in a specified amount of time.
----
----@param time number
----@param callback function
-function timer.simple( time, callback )
-	sortedinsert( backlog, { time = GetTime() + time - diff, callback = callback } )
-end
-
---- Creates a time to execute a function in the future
----
----@param id any
----@param interval number
----@param iterations number
----@param callback function
-function timer.create( id, interval, iterations, callback )
-	sortedinsert( backlog, {
-		id = id,
-		time = GetTime() + interval - diff,
-		interval = interval,
-		callback = callback,
-		runsleft = iterations - 1,
-	} )
-end
-
---- Waits a specified amount of time in a coroutine.
----
----@param time number
-function timer.wait( time )
-	local co = coroutine.running()
-	if not co then
-		error( "timer.wait() can only be used in a coroutine" )
-	end
-	timer.simple( time, function()
-		coroutine.resume( co )
-	end )
-	return coroutine.yield()
-end
-
-local function find( id )
-	for i = 1, #backlog do
-		if backlog[i].id == id then
-			return i, backlog[i]
-		end
-	end
-end
-
---- Gets the amount of time left of a named timer.
----
----@param id any
----@return number
-function timer.time_left( id )
-	local index, entry = find( id )
-	if entry then
-		return entry.time - GetTime()
-	end
-end
-
---- Gets the number of iterations left on a named timer.
----
----@param id any
----@return number
-function timer.iterations_left( id )
-	local index, entry = find( id )
-	if entry then
-		return entry.runsleft + 1
-	end
-end
-
---- Removes a named timer.
----
----@param id any
-function timer.remove( id )
-	local index, entry = find( id )
-	if index then
-		table.remove( backlog, index )
-	end
-end
-
-hook.add( "base.tick", "framework.timer", function( dt )
-	diff = 0
-	local now = GetTime()
-	while #backlog > 0 do
-		local first = backlog[#backlog]
-		if first.time > now then
-			break
-		end
-		backlog[#backlog] = nil
-		first.callback()
-		if first.runsleft and first.runsleft > 0 then
-			first.runsleft = first.runsleft - 1
-			first.time = first.time + first.interval
-			sortedinsert( backlog, first )
-		end
-	end
-end )
-
- end)();
---src/util/visual.lua
-(function() ----------------
--- Visual Utilities
--- @script util.visual
-visual = {}
-degreeToRadian = math.pi / 180
-COLOR_WHITE = { r = 255 / 255, g = 255 / 255, b = 255 / 255, a = 255 / 255 }
-COLOR_BLACK = { r = 0, g = 0, b = 0, a = 255 / 255 }
-COLOR_RED = { r = 255 / 255, g = 0, b = 0, a = 255 / 255 }
-COLOR_ORANGE = { r = 255 / 255, g = 128 / 255, b = 0, a = 255 / 255 }
-COLOR_YELLOW = { r = 255 / 255, g = 255 / 255, b = 0, a = 255 / 255 }
-COLOR_GREEN = { r = 0, g = 255 / 255, b = 0, a = 255 / 255 }
-COLOR_CYAN = { r = 0, g = 255 / 255, b = 128 / 255, a = 255 / 255 }
-COLOR_AQUA = { r = 0, g = 255 / 255, b = 255 / 255, a = 255 / 255 }
-COLOR_BLUE = { r = 0, g = 0, b = 255 / 255, a = 255 / 255 }
-COLOR_VIOLET = { r = 128 / 255, g = 0, b = 255 / 255, a = 255 / 255 }
-COLOR_PINK = { r = 255 / 255, g = 0, b = 255 / 255, a = 255 / 255 }
-
-if DrawSprite then
-	function visual.huergb( p, q, t )
-		if t < 0 then
-			t = t + 1
-		end
-		if t > 1 then
-			t = t - 1
-		end
-		if t < 1 / 6 then
-			return p + (q - p) * 6 * t
-		end
-		if t < 1 / 2 then
-			return q
-		end
-		if t < 2 / 3 then
-			return p + (q - p) * (2 / 3 - t) * 6
-		end
-		return p
-	end
-
-	--- Converts hue, saturation, and light to RGB.
-	---
-	---@param h number
-	---@param s number
-	---@param l number
-	---@return number[]
-	function visual.hslrgb( h, s, l )
-		local r, g, b
-
-		if s == 0 then
-			r = l
-			g = l
-			b = l
-		else
-			local huergb = visual.huergb
-
-			local q = l < .5 and l * (1 + s) or l + s - l * s
-			local p = 2 * l - q
-
-			r = huergb( p, q, h + 1 / 3 )
-			g = huergb( p, q, h )
-			b = huergb( p, q, h - 1 / 3 )
-
-		end
-		return Vec( r, g, b )
-	end
-
-	--- Draws a sprite facing the camera.
-	---
-	---@param sprite number
-	---@param source Vector
-	---@param radius number
-	---@param info table
-	function visual.drawsprite( sprite, source, radius, info )
-		local r, g, b, a
-		local writeZ, additive = true, false
-		local target = GetCameraTransform().pos
-		local DrawFunction = DrawSprite
-
-		radius = radius or 1
-
-		if info then
-			r = info.r and info.r or 1
-			g = info.g and info.g or 1
-			b = info.b and info.b or 1
-			a = info.a and info.a or 1
-			target = info.target or target
-			if info.writeZ ~= nil then
-				writeZ = info.writeZ
-			end
-			if info.additive ~= nil then
-				additive = info.additive
-			end
-			DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or DrawFunction
-		end
-
-		DrawFunction( sprite, Transform( source, QuatLookAt( source, target ) ), radius, radius, r, g, b, a, writeZ, additive )
-	end
-
-	--- Draws sprites facing the camera.
-	---
-	---@param sprites number[]
-	---@param sources Vector[]
-	---@param radius number
-	---@param info table
-	function visual.drawsprites( sprites, sources, radius, info )
-		sprites = type( sprites ) ~= "table" and { sprites } or sprites
-
-		for i = 1, #sprites do
-			for j = 1, #sources do
-				visual.drawsprite( sprites[i], sources[j], radius, info )
-			end
-		end
-	end
-
-	--- Draws a line using a sprite.
-	---
-	---@param sprite number
-	---@param source Vector
-	---@param destination Vector
-	---@param info table
-	function visual.drawline( sprite, source, destination, info )
-		local r, g, b, a
-		local writeZ, additive = true, false
-		local target = GetCameraTransform().pos
-		local DrawFunction = DrawLine
-		local width = 0.03
-
-		if info then
-			r = info.r and info.r or 1
-			g = info.g and info.g or 1
-			b = info.b and info.b or 1
-			a = info.a and info.a or 1
-			width = info.width or width
-			target = info.target or target
-			if info.writeZ ~= nil then
-				writeZ = info.writeZ
-			end
-			if info.additive ~= nil then
-				additive = info.additive
-			end
-			DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine)
-		end
-
-		if sprite then
-			local middle = VecScale( VecAdd( source, destination ), .5 )
-			local len = VecLength( VecSub( source, destination ) )
-			local transform = Transform( middle, QuatRotateQuat( QuatLookAt( source, destination ), QuatEuler( -90, 0, 0 ) ) )
-			local target_local = TransformToLocalPoint( transform, target )
-			target_local[2] = 0
-			local transform_fixed = TransformToParentTransform( transform, Transform( nil, QuatLookAt( target_local, nil ) ) )
-
-			DrawSprite( sprite, transform_fixed, width, len, r, g, b, a, writeZ, additive )
-		else
-			DrawFunction( source, destination, r, g, b, a );
-		end
-	end
-
-	--- Draws lines using a sprite.
-	---
-	---@param sprites number[] | number
-	---@param sources Vector[]
-	---@param connect boolean
-	---@param info table
-	function visual.drawlines( sprites, sources, connect, info )
-		sprites = type( sprites ) ~= "table" and { sprites } or sprites
-
-		for i = 1, #sprites do
-			local sourceCount = #sources
-
-			for j = 1, sourceCount - 1 do
-				visual.drawline( sprites[i], sources[j], sources[j + 1], info )
-			end
-
-			if connect then
-				visual.drawline( sprites[i], sources[1], sources[sourceCount], info )
-			end
-		end
-	end
-
-	--- Draws a debug axis.
-	---
-	---@param transform Transformation
-	---@param quat? Quaternion
-	---@param radius number
-	---@param writeZ boolean
-	function visual.drawaxis( transform, quat, radius, writeZ )
-		local DrawFunction = writeZ and DrawLine or DebugLine
-
-		if not transform.pos then
-			transform = Transform( transform, quat or QUAT_ZERO )
-		end
-		radius = radius or 1
-
-		DrawFunction( transform.pos, TransformToParentPoint( transform, Vec( radius, 0, 0 ) ), 1, 0, 0 )
-		DrawFunction( transform.pos, TransformToParentPoint( transform, Vec( 0, radius, 0 ) ), 0, 1, 0 )
-		DrawFunction( transform.pos, TransformToParentPoint( transform, Vec( 0, 0, radius ) ), 0, 0, 1 )
-	end
-
-	--- Draws a polygon.
-	---
-	---@param transform Transformation
-	---@param radius number
-	---@param rotation number
-	---@param sides number
-	---@param info table
-	function visual.drawpolygon( transform, radius, rotation, sides, info )
-		sides = sides or 4
-		radius = radius or 1
-
-		local offset, interval = math.rad( rotation or 0 ), 2 * math.pi / sides
-		local arc = false
-		local r, g, b, a = 1, 1, 1, 1
-		local DrawFunction = DrawLine
-
-		if info then
-			r = info.r or r
-			g = info.g or g
-			b = info.b or b
-			a = info.a or a
-			if info.arc then
-				arc = true
-				interval = interval * info.arc / 360
-			end
-			DrawFunction = info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine)
-		end
-
-		local points = {}
-		for i = 0, sides - 1 do
-			points[i + 1] = TransformToParentPoint( transform, Vec( math.sin( offset + i * interval ) * radius, 0,
-			                                                        math.cos( offset + i * interval ) * radius ) )
-			if i > 0 then
-				DrawFunction( points[i], points[i + 1], r, g, b, a )
-			end
-		end
-		if arc then
-			points[#points + 1] = TransformToParentPoint( transform, Vec( math.sin( offset + sides * interval ) * radius, 0,
-			                                                              math.cos( offset + sides * interval ) * radius ) )
-			DrawFunction( points[#points - 1], points[#points], r, g, b, a )
-		else
-			DrawFunction( points[#points], points[1], r, g, b, a )
-		end
-
-		return points
-	end
-
-	--- Draws a 3D box.
-	---
-	---@param transform Transformation
-	---@param min Vector
-	---@param max Vector
-	---@param info table
-	function visual.drawbox( transform, min, max, info )
-		local r, g, b, a
-		local DrawFunction = DrawLine
-		local points = {
-			TransformToParentPoint( transform, Vec( min[1], min[2], min[3] ) ),
-			TransformToParentPoint( transform, Vec( max[1], min[2], min[3] ) ),
-			TransformToParentPoint( transform, Vec( min[1], max[2], min[3] ) ),
-			TransformToParentPoint( transform, Vec( max[1], max[2], min[3] ) ),
-			TransformToParentPoint( transform, Vec( min[1], min[2], max[3] ) ),
-			TransformToParentPoint( transform, Vec( max[1], min[2], max[3] ) ),
-			TransformToParentPoint( transform, Vec( min[1], max[2], max[3] ) ),
-			TransformToParentPoint( transform, Vec( max[1], max[2], max[3] ) ),
-		}
-
-		if info then
-			r = info.r and info.r or 1
-			g = info.g and info.g or 1
-			b = info.b and info.b or 1
-			a = info.a and info.a or 1
-			DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine)
-		end
-
-		DrawFunction( points[1], points[2], r, g, b, a )
-		DrawFunction( points[1], points[3], r, g, b, a )
-		DrawFunction( points[1], points[5], r, g, b, a )
-		DrawFunction( points[4], points[3], r, g, b, a )
-		DrawFunction( points[4], points[2], r, g, b, a )
-		DrawFunction( points[4], points[8], r, g, b, a )
-		DrawFunction( points[6], points[5], r, g, b, a )
-		DrawFunction( points[6], points[8], r, g, b, a )
-		DrawFunction( points[6], points[2], r, g, b, a )
-		DrawFunction( points[7], points[8], r, g, b, a )
-		DrawFunction( points[7], points[5], r, g, b, a )
-		DrawFunction( points[7], points[3], r, g, b, a )
-
-		return points
-	end
-
-	--- Draws a prism.
-	---
-	---@param transform Transformation
-	---@param radius number
-	---@param depth number
-	---@param rotation number
-	---@param sides number
-	---@param info table
-	function visual.drawprism( transform, radius, depth, rotation, sides, info )
-		local points = {}
-		local iteration = 1
-		local pow, sqrt, sin, cos = math.pow, math.sqrt, math.sin, math.cos
-		local r, g, b, a
-		local DrawFunction = DrawLine
-
-		radius = sqrt( 2 * pow( radius, 2 ) ) or sqrt( 2 )
-		depth = depth or 1
-		rotation = rotation or 0
-		sides = sides or 4
-
-		if info then
-			r = info.r and info.r or 1
-			g = info.g and info.g or 1
-			b = info.b and info.b or 1
-			a = info.a and info.a or 1
-			DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine)
-		end
-
-		for v = 0, 360, 360 / sides do
-			points[iteration] = TransformToParentPoint( transform, Vec( sin( (v + rotation) * degreeToRadian ) * radius, depth,
-			                                                            cos( (v + rotation) * degreeToRadian ) * radius ) )
-			points[iteration + 1] = TransformToParentPoint( transform, Vec( sin( (v + rotation) * degreeToRadian ) * radius,
-			                                                                -depth,
-			                                                                cos( (v + rotation) * degreeToRadian ) * radius ) )
-			if iteration > 2 then
-				DrawFunction( points[iteration], points[iteration + 1], r, g, b, a )
-				DrawFunction( points[iteration - 2], points[iteration], r, g, b, a )
-				DrawFunction( points[iteration - 1], points[iteration + 1], r, g, b, a )
-			end
-			iteration = iteration + 2
-		end
-
-		return points
-	end
-
-	--- Draws a sphere.
-	---
-	---@param transform Transformation
-	---@param radius number
-	---@param rotation number
-	---@param samples number
-	---@param info table
-	function visual.drawsphere( transform, radius, rotation, samples, info )
-		local points = {}
-		local sqrt, sin, cos = math.sqrt, math.sin, math.cos
-		local r, g, b, a
-		local DrawFunction = DrawLine
-
-		radius = radius or 1
-		rotation = rotation or 0
-		samples = samples or 100
-
-		if info then
-			r = info.r and info.r or 1
-			g = info.g and info.g or 1
-			b = info.b and info.b or 1
-			a = info.a and info.a or 1
-			DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine)
-		end
-
-		-- Converted from python to lua, see original code https://stackoverflow.com/a/26127012/5459461
-		local points = {}
-		for i = 0, samples do
-			local y = 1 - (i / (samples - 1)) * 2
-			local rad = sqrt( 1 - y * y )
-			local theta = 2.399963229728653 * i
-
-			local x = cos( theta ) * rad
-			local z = sin( theta ) * rad
-			local point = TransformToParentPoint( Transform( transform.pos,
-			                                                 QuatRotateQuat( transform.rot, QuatEuler( 0, rotation, 0 ) ) ),
-			                                      Vec( x * radius, y * radius, z * radius ) )
-
-			DrawFunction( point, VecAdd( point, Vec( 0, .01, 0 ) ), r, g, b, a )
-			points[i + 1] = point
-		end
-
-		return points
-	end
-
-	--- Draws a wireframe sphere.
-	---
-	---@param transform Transformation
-	---@param radius number
-	---@param points number
-	---@param info table
-	function visual.drawwiresphere( transform, radius, points, info )
-		radius = radius or 1
-		points = points or 32
-		if not info or not info.nolines then
-			local tr_r = TransformToParentTransform( transform, Transform( Vec(), QuatEuler( 90, 0, 0 ) ) )
-			local tr_f = TransformToParentTransform( transform, Transform( Vec(), QuatEuler( 0, 0, 90 ) ) )
-			visual.drawpolygon( transform, radius, 0, points, info )
-			visual.drawpolygon( tr_r, radius, 0, points, info )
-			visual.drawpolygon( tr_f, radius, 0, points, info )
-		end
-
-		local cam = info and info.target or GetCameraTransform().pos
-		local diff = VecSub( transform.pos, cam )
-		local len = VecLength( diff )
-		if len < radius then
-			return
-		end
-		local a = math.pi / 2 - math.asin( radius / len )
-		local vtr = Transform( VecAdd( transform.pos, VecScale( diff, -math.cos( a ) / len ) ),
-		                       QuatRotateQuat( QuatLookAt( transform.pos, cam ), QuatEuler( 90, 0, 0 ) ) )
-		visual.drawpolygon( vtr, radius * math.sin( a ), 0, points, info )
-	end
-end
-
- end)();
---src/util/xml.lua
-(function() ----------------
--- XML Utilities
--- @script util.xml
-
----@class XMLNode
----@field __call fun(children: XMLNode[]): XMLNode
----@field attributes table<string, string> | nil
----@field children XMLNode[] | nil
----@field type string
-local xml_meta
-xml_meta = global_metatable( "xmlnode" )
-
---- Defines an XML node.
----
----@param type string
----@return fun(attributes: table<string, string>): XMLNode
-XMLTag = function( type )
-	return function( attributes )
-		return setmetatable( { type = type, attributes = attributes }, xml_meta )
-	end
-end
-
---- Parses XML from a string.
----
----@param xml string
----@return XMLNode
-ParseXML = function( xml )
-	local pos = 1
-	local function skipw()
-		local next = xml:find( "[^ \t\n]", pos )
-		if not next then
-			return false
-		end
-		pos = next
-		return true
-	end
-	local function expect( pattern, noskip )
-		if not noskip then
-			if not skipw() then
-				return false
-			end
-		end
-		local s, e = xml:find( pattern, pos )
-		if not s then
-			return false
-		end
-		local pre = pos
-		pos = e + 1
-		return xml:match( pattern, pre )
-	end
-
-	local readtag, readattribute, readstring
-
-	local rt = { n = "\n", t = "\t", r = "\r", ["0"] = "\0", ["\\"] = "\\", ["\""] = "\"" }
-	readstring = function()
-		if not expect( "^\"" ) then
-			return false
-		end
-		local start = pos
-		while true do
-			local s = assert( xml:find( "[\\\"]", pos ), "Invalid string" )
-			if xml:sub( s, s ) == "\\" then
-				pos = s + 2
-			else
-				pos = s + 1
-				break
-			end
-		end
-		return xml:sub( start, pos - 2 ):gsub( "\\(.)", rt )
-	end
-
-	readattribute = function()
-		local name = expect( "^([%d%w_]+)" )
-		if not name then
-			return false
-		end
-		if expect( "^=" ) then
-			return name, assert( readstring() )
-		else
-			return name, "1"
-		end
-	end
-
-	readtag = function()
-		local save = pos
-		if not expect( "^<" ) then
-			return false
-		end
-
-		local type = expect( "^([%d%w_]+)" )
-		if not type then
-			pos = save
-			return false
-		end
-		skipw()
-
-		local attributes = {}
-		repeat
-			local attr, val = readattribute()
-			if attr then
-				attributes[attr] = val
-			end
-		until not attr
-
-		local children = {}
-		if not expect( "^/>" ) then
-			assert( expect( "^>" ) )
-			repeat
-				local child = readtag()
-				if child then
-					children[#children + 1] = child
-				end
-			until not child
-			assert( expect( "^</" ) and expect( "^" .. type ) and expect( "^>" ) )
-		end
-
-		return XMLTag( type )( attributes )( children )
-	end
-
-	return readtag()
-end
-
----@type XMLNode
-
----@return XMLNode self
-function xml_meta:__call( children )
-	self.children = children
-	return self
-end
-
---- Renders this node into an XML string.
----
----@return string
-function xml_meta:Render()
-	local attr = ""
-	if self.attributes then
-		for name, val in pairs( self.attributes ) do
-			attr = string.format( "%s %s=%q", attr, name, val )
-		end
-	end
-	local children = {}
-	if self.children then
-		for i = 1, #self.children do
-			children[i] = self.children[i]:Render()
-		end
-	end
-	return string.format( "<%s%s>%s</%s>", self.type, attr, table.concat( children, "" ), self.type )
-end
-
- end)();
---src/vector/quat.lua
-(function() ----------------
--- Quaternion class and related functions
--- @script vector.quat
-
-local vector_meta = global_metatable( "vector" )
----@class Quaternion
-local quat_meta
-quat_meta = global_metatable( "quaternion" )
-
---- Tests if the parameter is a quaternion.
----
----@param q any
----@return boolean
-function IsQuaternion( q )
-	return type( q ) == "table" and type( q[1] ) == "number" and type( q[2] ) == "number" and type( q[3] ) == "number" and
-		       type( q[4] ) == "number"
-end
-
---- Makes the parameter quat into a quaternion.
----
----@param q number[]
----@return Quaternion q
-function MakeQuaternion( q )
-	return setmetatable( q, quat_meta )
-end
-
---- Creates a new quaternion.
----
----@param i? number
----@param j? number
----@param k? number
----@param r? number
----@return Quaternion
----@overload fun(q: Quaternion): Quaternion
-function Quaternion( i, j, k, r )
-	if IsQuaternion( i ) then
-		i, j, k, r = i[1], i[2], i[3], i[4]
-	end
-	return MakeQuaternion { i or 0, j or 0, k or 0, r or 1 }
-end
-
----@type Quaternion
-
----@param data string
----@return Quaternion self
-function quat_meta:__unserialize( data )
-	local i, j, k, r = data:match( "([-0-9.]*);([-0-9.]*);([-0-9.]*);([-0-9.]*)" )
-	self[1] = tonumber( i )
-	self[2] = tonumber( j )
-	self[3] = tonumber( k )
-	self[4] = tonumber( r )
-	return self
-end
-
----@return string data
-function quat_meta:__serialize()
-	return table.concat( self, ";" )
-end
-
-QUAT_ZERO = Quaternion()
-
---- Clones the quaternion.
----
----@return Quaternion clone
-function quat_meta:Clone()
-	return MakeQuaternion { self[1], self[2], self[3], self[4] }
-end
-
-local QuatStr = QuatStr
----@return string
-function quat_meta:__tostring()
-	return QuatStr( self )
-end
-
----@return Quaternion
-function quat_meta:__unm()
-	return MakeQuaternion { -self[1], -self[2], -self[3], -self[4] }
-end
-
---- Conjugates the quaternion.
----
----@return Quaternion
-function quat_meta:Conjugate()
-	return MakeQuaternion { -self[1], -self[2], -self[3], self[4] }
-end
-
---- Inverts the quaternion.
----
----@return Quaternion
-function quat_meta:Invert()
-	local l = quat_meta.LengthSquare( self )
-	return MakeQuaternion { -self[1] / l, -self[2] / l, -self[3] / l, self[4] / l }
-end
-
---- Adds to the quaternion.
----
----@param o Quaternion | number
----@return Quaternion self
-function quat_meta:Add( o )
-	if IsQuaternion( o ) then
-		self[1] = self[1] + o[1]
-		self[2] = self[2] + o[2]
-		self[3] = self[3] + o[3]
-		self[4] = self[4] + o[4]
-	else
-		self[1] = self[1] + o
-		self[2] = self[2] + o
-		self[3] = self[3] + o
-		self[4] = self[4] + o
-	end
-	return self
-end
-
----@param a Quaternion | number
----@param b Quaternion | number
----@return Quaternion
-function quat_meta.__add( a, b )
-	if not IsQuaternion( a ) then
-		a, b = b, a
-	end
-	return quat_meta.Add( quat_meta.Clone( a ), b )
-end
-
---- Subtracts from the quaternion.
----
----@param o Quaternion | number
----@return Quaternion self
-function quat_meta:Sub( o )
-	if IsQuaternion( o ) then
-		self[1] = self[1] - o[1]
-		self[2] = self[2] - o[2]
-		self[3] = self[3] - o[3]
-		self[4] = self[4] - o[4]
-	else
-		self[1] = self[1] - o
-		self[2] = self[2] - o
-		self[3] = self[3] - o
-		self[4] = self[4] - o
-	end
-	return self
-end
-
----@param a Quaternion | number
----@param b Quaternion | number
----@return Quaternion
-function quat_meta.__sub( a, b )
-	if not IsQuaternion( a ) then
-		a, b = b, a
-	end
-	return quat_meta.Sub( quat_meta.Clone( a ), b )
-end
-
---- Multiplies (~rotate) the quaternion.
----
----@param o Quaternion
----@return Quaternion self
-function quat_meta:Mul( o )
-	local i1, j1, k1, r1 = self[1], self[2], self[3], self[4]
-	local i2, j2, k2, r2 = o[1], o[2], o[3], o[4]
-	self[1] = j1 * k2 - k1 * j2 + r1 * i2 + i1 * r2
-	self[2] = k1 * i2 - i1 * k2 + r1 * j2 + j1 * r2
-	self[3] = i1 * j2 - j1 * i2 + r1 * k2 + k1 * r2
-	self[4] = r1 * r2 - i1 * i2 - j1 * j2 - k1 * k2
-	return self
-end
-
----@param a Quaternion | number
----@param b Quaternion | number
----@return Quaternion
----@overload fun(a: Quaternion, b: Vector): Vector
----@overload fun(a: Quaternion, b: Transformation): Transformation
-function quat_meta.__mul( a, b )
-	if not IsQuaternion( a ) then
-		a, b = b, a
-	end
-	if type( b ) == "number" then
-		return Quaternion( a[1] * b, a[2] * b, a[3] * b, a[4] * b )
-	end
-	if IsVector( b ) then
-		return vector_meta.__mul( b, a )
-	end
-	if IsTransformation( b ) then
-		---@diagnostic disable-next-line: undefined-field
-		return Transformation( vector_meta.Mul( vector_meta.Clone( b.pos ), a ), QuatRotateQuat( b.rot, a ) )
-	end
-	return MakeQuaternion( QuatRotateQuat( a, b ) )
-end
-
---- Divides the quaternion components.
----
----@param o number
----@return Quaternion self
-function quat_meta:Div( o )
-	if IsQuaternion( o ) then
-		quat_meta.Mul( self, { -o[1], -o[2], -o[3], o[4] } )
-	else
-		self[1] = self[1] / o
-		self[2] = self[2] / o
-		self[3] = self[3] / o
-		self[4] = self[4] / o
-	end
-	return self
-end
-
----@param a Quaternion | number
----@param b Quaternion | number
----@return Quaternion
-function quat_meta.__div( a, b )
-	return quat_meta.Div( quat_meta.Clone( a ), b )
-end
-
----@param a Quaternion
----@param b Quaternion
----@return boolean
-function quat_meta.__eq( a, b )
-	return a[1] == b[1] and a[2] == b[2] and a[3] == b[3] and a[4] == b[4]
-end
-
---- Gets the squared length of the quaternion.
----
----@return number
-function quat_meta:LengthSquare()
-	return self[1] ^ 2 + self[2] ^ 2 + self[3] ^ 2 + self[4] ^ 2
-end
-
---- Gets the length of the quaternion
----
----@return number
-function quat_meta:Length()
-	return math.sqrt( quat_meta.LengthSquare( self ) )
-end
-
-local QuatSlerp = QuatSlerp
---- S-lerps from the quaternion to another one.
----
----@param o Quaternion
----@param n number
----@return Quaternion
-function quat_meta:Slerp( o, n )
-	return MakeQuaternion( QuatSlerp( self, o, n ) )
-end
-
---- Gets the left-direction of the quaternion.
----
----@return Vector
-function quat_meta:Left()
-	local x, y, z, s = self[1], self[2], self[3], self[4]
-
-	return Vector( 1 - (y ^ 2 + z ^ 2) * 2, (z * s + x * y) * 2, (x * z - y * s) * 2 )
-end
-
---- Gets the up-direction of the quaternion.
----
----@return Vector
-function quat_meta:Up()
-	local x, y, z, s = self[1], self[2], self[3], self[4]
-
-	return Vector( (y * x - z * s) * 2, 1 - (z ^ 2 + x ^ 2) * 2, (x * s + y * z) * 2 )
-end
-
---- Gets the forward-direction of the quaternion.
----
----@return Vector
-function quat_meta:Forward()
-	local x, y, z, s = self[1], self[2], self[3], self[4]
-
-	return Vector( (y * s + z * x) * 2, (z * y - x * s) * 2, 1 - (x ^ 2 + y ^ 2) * 2 )
-end
-
---- Gets the euler angle representation of the quaternion.
---- Note: This uses the same order as QuatEuler().
----
----@return number
----@return number
----@return number
-function quat_meta:ToEuler()
-	if GetQuatEuler then
-		return GetQuatEuler( self )
-	end
-	local x, y, z, w = self[1], self[2], self[3], self[4]
-	-- Credit to https://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToEuler/index.htm
-
-	local bank, heading, attitude
-
-	local s = 2 * x * y + 2 * z * w
-	if s >= 1 then
-		heading = 2 * math.atan2( x, w )
-		bank = 0
-		attitude = math.pi / 2
-	elseif s <= -1 then
-		heading = -2 * math.atan2( x, w )
-		bank = 0
-		attitude = math.pi / -2
-	else
-		bank = math.atan2( 2 * x * w - 2 * y * z, 1 - 2 * x ^ 2 - 2 * z ^ 2 )
-		heading = math.atan2( 2 * y * w - 2 * x * z, 1 - 2 * y ^ 2 - 2 * z ^ 2 )
-		attitude = math.asin( s )
-	end
-
-	return math.deg( bank ), math.deg( heading ), math.deg( attitude )
-end
-
---- Approachs another quaternion by the specified angle.
----
----@param dest Quaternion
----@param rate number
----@return Quaternion
-function quat_meta:Approach( dest, rate )
-	local dot = self[1] * dest[1] + self[2] * dest[2] + self[3] * dest[3] + self[4] * dest[4]
-	if dot >= 1 then
-		return self
-	end
-	local corr_rate = rate / math.acos( 2 * dot ^ 2 - 1 )
-	if corr_rate >= 1 then
-		return MakeQuaternion( dest )
-	end
-	return MakeQuaternion( QuatSlerp( self, dest, corr_rate ) )
-end
-
- end)();
---src/vector/transform.lua
-(function() ----------------
--- Transform class and related functions
--- @script vector.transform
-
-local vector_meta = global_metatable( "vector" )
-local quat_meta = global_metatable( "quaternion" )
----@class Transformation
----@field pos Vector
----@field rot Quaternion
-local transform_meta
-transform_meta = global_metatable( "transformation" )
-
---- Tests if the parameter is a transformation.
----
----@param t any
----@return boolean
-function IsTransformation( t )
-	return type( t ) == "table" and t.pos and t.rot
-end
-
---- Makes the parameter transform into a transformation.
----
----@param t { pos: number[] | Vector, rot: number[] | Quaternion }
----@return Transformation t
-function MakeTransformation( t )
-	setmetatable( t.pos, vector_meta )
-	setmetatable( t.rot, quat_meta )
-	return setmetatable( t, transform_meta )
-end
-
---- Creates a new transformation.
----
----@param pos number[] | Vector
----@param rot number[] | Quaternion
----@return Transformation
-function Transformation( pos, rot )
-	return MakeTransformation { pos = pos, rot = rot }
-end
-
----@type Transformation
-
----@param data string
----@return Transformation self
-function transform_meta:__unserialize( data )
-	local x, y, z, i, j, k, r =
-		data:match( "([-0-9.]*);([-0-9.]*);([-0-9.]*);([-0-9.]*);([-0-9.]*);([-0-9.]*);([-0-9.]*)" )
-	self.pos = Vector( tonumber( x ), tonumber( y ), tonumber( z ) )
-	self.rot = Quaternion( tonumber( i ), tonumber( j ), tonumber( k ), tonumber( r ) )
-	return self
-end
-
----@return string data
-function transform_meta:__serialize()
-	return table.concat( self.pos, ";" ) .. ";" .. table.concat( self.rot, ";" )
-end
-
---- Clones the transformation.
----
----@return Vector clone
-function transform_meta:Clone()
-	return MakeTransformation { pos = vector_meta.Clone( self.pos ), rot = quat_meta.Clone( self.rot ) }
-end
-
-local TransformStr = TransformStr
----@return string
-function transform_meta:__tostring()
-	return TransformStr( self )
-end
-
-local TransformToLocalPoint = TransformToLocalPoint
-local TransformToLocalTransform = TransformToLocalTransform
-local TransformToLocalVec = TransformToLocalVec
-local TransformToParentPoint = TransformToParentPoint
-local TransformToParentTransform = TransformToParentTransform
-local TransformToParentVec = TransformToParentVec
-
----@param a Transformation
----@param b Transformation | Vector | Quaternion
----@return Transformation
-function transform_meta.__add( a, b )
-	if not IsTransformation( b ) then
-		if IsVector( b ) then
-			b = Transformation( b, QUAT_ZERO )
-		elseif IsQuaternion( b ) then
-			b = Transformation( VEC_ZERO, b )
-		end
-	end
-	return MakeTransformation( TransformToParentTransform( a, b ) )
-end
-
---- Gets the local representation of a world-space transform, point or rotation
----
----@param o Transformation
----@return Transformation
----@overload fun(o: Vector): Vector
----@overload fun(o: Quaternion): Quaternion
-function transform_meta:ToLocal( o )
-	if IsTransformation( o ) then
-		return MakeTransformation( TransformToLocalTransform( self, o ) )
-	elseif IsQuaternion( o ) then
-		return MakeQuaternion( TransformToLocalTransform( self, Transform( {}, o ) ).rot )
-	else
-		return MakeVector( TransformToLocalPoint( self, o ) )
-	end
-end
-
---- Gets the local representation of a world-space direction
----
----@param o Vector
----@return Vector
-function transform_meta:ToLocalDir( o )
-	return MakeVector( TransformToLocalVec( self, o ) )
-end
-
---- Gets the global representation of a local-space transform, point or rotation
----
----@param o Transformation
----@return Transformation
----@overload fun(o: Vector): Vector
----@overload fun(o: Quaternion): Quaternion
-function transform_meta:ToGlobal( o )
-	if IsTransformation( o ) then
-		return MakeTransformation( TransformToParentTransform( self, o ) )
-	elseif IsQuaternion( o ) then
-		return MakeQuaternion( TransformToParentTransform( self, Transform( {}, o ) ).rot )
-	else
-		return MakeVector( TransformToParentPoint( self, o ) )
-	end
-end
-
---- Gets the global representation of a local-space direction
----
----@param o Vector
----@return Vector
-function transform_meta:ToGlobalDir( o )
-	return MakeVector( TransformToParentVec( self, o ) )
-end
-
---- Raycasts from the transformation
----
----@param dist number
----@param mul? number
----@param radius? number
----@param rejectTransparent? boolean
----@return { hit: boolean, dist: number, normal: Vector, shape: Shape | number, hitpos: Vector }
-function transform_meta:Raycast( dist, mul, radius, rejectTransparent )
-	local dir = TransformToParentVec( self, VEC_FORWARD )
-	if mul then
-		vector_meta.Mul( dir, mul )
-	end
-	local hit, dist2, normal, shape = QueryRaycast( self.pos, dir, dist, radius, rejectTransparent )
-	return {
-		hit = hit,
-		dist = dist2,
-		normal = hit and MakeVector( normal ),
-		shape = hit and Shape and Shape( shape ) or shape,
-		hitpos = vector_meta.__add( self.pos, vector_meta.Mul( dir, hit and dist2 or dist ) ),
-	}
-end
-
- end)();
---src/vector/vector.lua
-(function() ----------------
--- Vector class and related functions
--- @script vector.vector
-
-local quat_meta = global_metatable( "quaternion" )
-
----@class Vector
-local vector_meta
-vector_meta = global_metatable( "vector" )
-
---- Tests if the parameter is a vector.
----
----@param v any
----@return boolean
-function IsVector( v )
-	return type( v ) == "table" and type( v[1] ) == "number" and type( v[2] ) == "number" and type( v[3] ) == "number" and
-		       not v[4]
-end
-
---- Makes the parameter vec into a vector.
----
----@param v number[]
----@return Vector v
-function MakeVector( v )
-	return setmetatable( v, vector_meta )
-end
-
---- Creates a new vector.
----
----@param x? number
----@param y? number
----@param z? number
----@return Vector
----@overload fun(v: Vector): Vector
-function Vector( x, y, z )
-	if IsVector( x ) then
-		x, y, z = x[1], x[2], x[3]
-	end
-	return MakeVector { x or 0, y or 0, z or 0 }
-end
-
----@type Vector
-
----@param data string
----@return Vector self
-function vector_meta:__unserialize( data )
-	local x, y, z = data:match( "([-0-9.]*);([-0-9.]*);([-0-9.]*)" )
-	self[1] = tonumber( x )
-	self[2] = tonumber( y )
-	self[3] = tonumber( z )
-	return self
-end
-
----@return string data
-function vector_meta:__serialize()
-	return table.concat( self, ";" )
-end
-
-VEC_ZERO = Vector()
-VEC_FORWARD = Vector( 0, 0, 1 )
-VEC_UP = Vector( 0, 1, 0 )
-VEC_LEFT = Vector( 1, 0, 0 )
-
---- Clones the vector.
----
----@return Vector clone
-function vector_meta:Clone()
-	return MakeVector { self[1], self[2], self[3] }
-end
-
-local VecStr = VecStr
----@return string
-function vector_meta:__tostring()
-	return VecStr( self )
-end
-
----@return Vector
-function vector_meta:__unm()
-	return MakeVector { -self[1], -self[2], -self[3] }
-end
-
---- Adds to the vector.
----
----@param o Vector | number
----@return Vector self
-function vector_meta:Add( o )
-	if IsVector( o ) then
-		self[1] = self[1] + o[1]
-		self[2] = self[2] + o[2]
-		self[3] = self[3] + o[3]
-	else
-		self[1] = self[1] + o
-		self[2] = self[2] + o
-		self[3] = self[3] + o
-	end
-	return self
-end
-
----@param a Vector | Transformation | number
----@param b Vector | Transformation | number
----@return Vector
-function vector_meta.__add( a, b )
-	if not IsVector( a ) then
-		a, b = b, a
-	end
-	if IsTransformation( b ) then
-		return Transformation( vector_meta.Add( vector_meta.Clone( a ), b.pos ), quat_meta.Clone( b.rot ) )
-	end
-	return vector_meta.Add( vector_meta.Clone( a ), b )
-end
-
---- Subtracts from the vector.
----
----@param o Vector | number
----@return Vector self
-function vector_meta:Sub( o )
-	if IsVector( o ) then
-		self[1] = self[1] - o[1]
-		self[2] = self[2] - o[2]
-		self[3] = self[3] - o[3]
-	else
-		self[1] = self[1] - o
-		self[2] = self[2] - o
-		self[3] = self[3] - o
-	end
-	return self
-end
-
----@param a Vector | number
----@param b Vector | number
----@return Vector
-function vector_meta.__sub( a, b )
-	if not IsVector( a ) then
-		a, b = b, a
-	end
-	return vector_meta.Sub( vector_meta.Clone( a ), b )
-end
-
---- Multiplies the vector.
----
----@param o Vector | Quaternion | number
----@return Vector self
-function vector_meta:Mul( o )
-	if IsVector( o ) then
-		self[1] = self[1] * o[1]
-		self[2] = self[2] * o[2]
-		self[3] = self[3] * o[3]
-	elseif IsQuaternion( o ) then
-		-- v2 = v + 2 * r X (s * v + r X v) / quat_meta.LengthSquare(self)
-		-- local s, r = o[4], Vector(o[1], o[2], o[3])
-		-- self:Add(2 * s * r:Cross(self) + 2 * r:Cross(r:Cross(self)))
-
-		local x1, y1, z1 = self[1], self[2], self[3]
-		local x2, y2, z2, s = o[1], o[2], o[3], o[4]
-
-		local x3 = y2 * z1 - z2 * y1
-		local y3 = z2 * x1 - x2 * z1
-		local z3 = x2 * y1 - y2 * x1
-
-		self[1] = x1 + (x3 * s + y2 * z3 - z2 * y3) * 2
-		self[2] = y1 + (y3 * s + z2 * x3 - x2 * z3) * 2
-		self[3] = z1 + (z3 * s + x2 * y3 - y2 * x3) * 2
-	else
-		self[1] = self[1] * o
-		self[2] = self[2] * o
-		self[3] = self[3] * o
-	end
-	return self
-end
-
----@param a Vector | Quaternion | number
----@param b Vector | Quaternion | number
----@return Vector
-function vector_meta.__mul( a, b )
-	if not IsVector( a ) then
-		a, b = b, a
-	end
-	return vector_meta.Mul( vector_meta.Clone( a ), b )
-end
-
---- Divides the vector components.
----
----@param o number
----@return Vector self
-function vector_meta:Div( o )
-	self[1] = self[1] / o
-	self[2] = self[2] / o
-	self[3] = self[3] / o
-	return self
-end
-
----@param a Vector | number
----@param b Vector | number
----@return Vector
-function vector_meta.__div( a, b )
-	return vector_meta.Div( vector_meta.Clone( a ), b )
-end
-
---- Applies the modulo operator on the vector components.
----
----@param o number
----@return Vector self
-function vector_meta:Mod( o )
-	self[1] = self[1] % o
-	self[2] = self[2] % o
-	self[3] = self[3] % o
-	return self
-end
-
----@param a Vector | number
----@param b Vector | number
----@return Vector
-function vector_meta.__mod( a, b )
-	return vector_meta.Mod( vector_meta.Clone( a ), b )
-end
-
---- Applies the exponent operator on the vector components.
----
----@param o number
----@return Vector self
-function vector_meta:Pow( o )
-	self[1] = self[1] ^ o
-	self[2] = self[2] ^ o
-	self[3] = self[3] ^ o
-	return self
-end
-
----@param a Vector
----@param b number
----@return Vector
-function vector_meta.__pow( a, b )
-	return vector_meta.Pow( vector_meta.Clone( a ), b )
-end
-
----@param a Vector
----@param b Vector
----@return boolean
-function vector_meta.__eq( a, b )
-	return a[1] == b[1] and a[2] == b[2] and a[3] == b[3]
-end
-
----@param a Vector
----@param b Vector
----@return boolean
-function vector_meta.__lt( a, b )
-	return a[1] < b[1] or (a[1] == b[1] and (a[2] < b[2] or (a[2] == b[2] and (a[3] < b[3]))))
-end
-
----@param a Vector
----@param b Vector
----@return boolean
-function vector_meta.__le( a, b )
-	return a[1] < b[1] or (a[1] == b[1] and (a[2] < b[2] or (a[2] == b[2] and (a[3] <= b[3]))))
-end
-
-local VecDot = VecDot
---- Computes the dot product with another vector.
----
----@param b Vector
----@return number
-function vector_meta:Dot( b )
-	return VecDot( self, b )
-end
-
-local VecCross = VecCross
---- Computes the cross product with another vector.
----
----@param b Vector
----@return Vector
-function vector_meta:Cross( b )
-	return MakeVector( VecCross( self, b ) )
-end
-
-local VecLength = VecLength
---- Gets the length of the vector.
----
----@return number
-function vector_meta:Length()
-	return VecLength( self )
-end
-
---- Gets the volume of the vector (product of all its components).
----
----@return number
-function vector_meta:Volume()
-	return math.abs( self[1] * self[2] * self[3] )
-end
-
-local VecLerp = VecLerp
---- Lerps from the vector to another one.
----
----@param o Vector
----@param n number
----@return Vector
-function vector_meta:Lerp( o, n )
-	return MakeVector( VecLerp( self, o, n ) )
-end
-
-local VecNormalize = VecNormalize
---- Gets the normalized form of the vector.
----
----@return Vector
-function vector_meta:Normalized()
-	return MakeVector( VecNormalize( self ) )
-end
-
---- Normalize the vector.
----
----@return Vector self
-function vector_meta:Normalize()
-	return vector_meta.Div( self, vector_meta.Length( self ) )
-end
-
---- Gets the squared distance to another vector.
----
----@return number
-function vector_meta:DistSquare( o )
-	return (self[1] - o[1]) ^ 2 + (self[2] - o[2]) ^ 2 + (self[3] - o[3]) ^ 2
-end
-
---- Gets the distance to another vector.
----
----@return number
-function vector_meta:Distance( o )
-	return math.sqrt( vector_meta.DistSquare( self, o ) )
-end
-
---- Gets the rotation to another vector.
----
----@param o Vector
----@return Quaternion
-function vector_meta:LookAt( o )
-	return MakeQuaternion( QuatLookAt( self, o ) )
-end
-
---- Approachs another vector by the specified distance.
----
----@param dest Vector
----@param rate number
----@return Vector
-function vector_meta:Approach( dest, rate )
-	local dist = vector_meta.Distance( self, dest )
-	if dist < rate then
-		return dest
-	end
-	return vector_meta.Lerp( self, dest, rate / dist )
-end
-
---- Get the minimum value for each vector component.
----
----@vararg Vector
----@return Vector
----@overload fun(o: number, ...): Vector
-function vector_meta:Min( ... )
-	local n = vector_meta.Clone( self )
-	for i = 1, select( "#", ... ) do
-		local o = select( i, ... )
-		if type( o ) == "number" then
-			n[1] = math.min( n[1], o )
-			n[2] = math.min( n[2], o )
-			n[3] = math.min( n[3], o )
-		else
-			n[1] = math.min( n[1], o[1] )
-			n[2] = math.min( n[2], o[2] )
-			n[3] = math.min( n[3], o[3] )
-		end
-	end
-	return n
-end
-
---- Get the maximum value for each vector component.
----
----@vararg Vector
----@return Vector
----@overload fun(o: number, ...): Vector
-function vector_meta:Max( ... )
-	local n = vector_meta.Clone( self )
-	for i = 1, select( "#", ... ) do
-		local o = select( i, ... )
-		if type( o ) == "number" then
-			n[1] = math.max( n[1], o )
-			n[2] = math.max( n[2], o )
-			n[3] = math.max( n[3], o )
-		else
-			n[1] = math.max( n[1], o[1] )
-			n[2] = math.max( n[2], o[2] )
-			n[3] = math.max( n[3], o[3] )
-		end
-	end
-	return n
-end
-
---- Clamp the vector components.
----
----@param min Vector | number
----@param max Vector | number
----@return Vector
-function vector_meta:Clamp( min, max )
-	if type( min ) == "number" then
-		return Vector( math.max( math.min( self[1], max ), min ), math.max( math.min( self[2], max ), min ),
-		               math.max( math.min( self[3], max ), min ) )
-	else
-		return Vector( math.max( math.min( self[1], max[1] ), min[1] ), math.max( math.min( self[2], max[2] ), min[2] ),
-		               math.max( math.min( self[3], max[3] ), min[3] ) )
-	end
-end
-
- end)();
---src/entities/entity.lua
-(function() ----------------
--- Entity class and related functions
--- @script entities.entity
-
----@class Entity
----@field handle number
----@field type string
-local entity_meta
-entity_meta = global_metatable( "entity" )
-
---- Gets the handle of an entity.
----
----@param e Entity | number
----@return number
-function GetEntityHandle( e )
-	if IsEntity( e ) then
-		return e.handle
-	end
-	return e
-end
-
---- Gets the validity of a table by calling :IsValid() if it supports it.
----
----@param e any
----@return boolean
-function IsValid( e )
-	if type( e ) == "table" and e.IsValid then
-		return e:IsValid()
-	end
-	return false
-end
-
---- Tests if the parameter is an entity.
----
----@param e any
----@return boolean
-function IsEntity( e )
-	return type( e ) == "table" and type( e.handle ) == "number"
-end
-
---- Wraps the given handle with the entity class.
----
----@param handle number
----@return Entity
-function Entity( handle )
-	if handle > 0 then
-		return setmetatable( { handle = handle, type = "unknown" }, entity_meta )
-	end
-end
-
----@type Entity
-
----@param data string
----@return Entity self
-function entity_meta:__unserialize( data )
-	self.handle = tonumber( data )
-	return self
-end
-
----@return string data
-function entity_meta:__serialize()
-	return tostring( self.handle )
-end
-
----@return string
-function entity_meta:__tostring()
-	return string.format( "Entity[%d]", self.handle )
-end
-
---- Gets the type of the entity.
----
----@return string type
-function entity_meta:GetType()
-	return self.type or "unknown"
-end
-
-local IsHandleValid = IsHandleValid
---- Gets the validity of the entity.
----
----@return boolean
-function entity_meta:IsValid()
-	return IsHandleValid( self.handle )
-end
-
-local SetTag = SetTag
---- Sets a tag value on the entity.
----
----@param tag string
----@param value string
-function entity_meta:SetTag( tag, value )
-	assert( self:IsValid() )
-	return SetTag( self.handle, tag, value )
-end
-
-local SetDescription = SetDescription
---- Sets the description of the entity.
----
----@param description string
-function entity_meta:SetDescription( description )
-	assert( self:IsValid() )
-	return SetDescription( self.handle, description )
-end
-
-local RemoveTag = RemoveTag
---- Removes a tag from the entity.
----
----@param tag string
-function entity_meta:RemoveTag( tag )
-	assert( self:IsValid() )
-	return RemoveTag( self.handle, tag )
-end
-
-local HasTag = HasTag
---- Gets if the entity has a tag.
----
----@param tag string
----@return boolean
-function entity_meta:HasTag( tag )
-	assert( self:IsValid() )
-	return HasTag( self.handle, tag )
-end
-
-local GetTagValue = GetTagValue
---- Gets the value of a tag.
----
----@param tag string
----@return string
-function entity_meta:GetTagValue( tag )
-	assert( self:IsValid() )
-	return GetTagValue( self.handle, tag )
-end
-
-local GetDescription = GetDescription
---- Gets the description of the entity.
----
----@return string
-function entity_meta:GetDescription()
-	assert( self:IsValid() )
-	return GetDescription( self.handle )
-end
-
-local Delete = Delete
---- Deletes the entity.
-function entity_meta:Delete()
-	return Delete( self.handle )
-end
-
- end)();
---src/entities/body.lua
-(function() ----------------
--- Body class and related functions
--- @script entities.body
-
----@class Body: Entity
-local body_meta
-body_meta = global_metatable( "body", "entity" )
-
---- Tests if the parameter is a body entity.
----
----@param e any
----@return boolean
-function IsBody( e )
-	return IsEntity( e ) and e.type == "body"
-end
-
---- Wraps the given handle with the body class.
----
----@param handle number
----@return Body?
-function Body( handle )
-	if handle > 0 then
-		return setmetatable( { handle = handle, type = "body" }, body_meta )
-	end
-end
-
---- Finds a body with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Body?
-function FindBodyByTag( tag, global )
-	return Body( FindBody( tag, global ) )
-end
-
---- Finds all bodies with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Body[]
-function FindBodiesByTag( tag, global )
-	local t = FindBodies( tag, global )
-	for i = 1, #t do
-		t[i] = Body( t[i] )
-	end
-	return t
-end
-
----@type Body
-
----@return string
-function body_meta:__tostring()
-	return string.format( "Body[%d]", self.handle )
-end
-
---- Applies a force to the body at the specified world-space point.
----
----@param pos Vector World-space position
----@param vel Vector World-space force and direction
-function body_meta:ApplyImpulse( pos, vel )
-	assert( self:IsValid() )
-	return ApplyBodyImpulse( self.handle, pos, vel )
-end
-
---- Applies a force to the body at the specified object-space point.
----
----@param pos Vector Object-space position
----@param vel Vector Object-space force and direction
-function body_meta:ApplyLocalImpulse( pos, vel )
-	local transform = self:GetTransform()
-	return self:ApplyImpulse( transform:ToGlobal( pos ), transform:ToGlobalDir( vel ) )
-end
-
---- Draws the outline of the body.
----
----@param r number
----@overload fun(r: number, g: number, b: number, a: number)
-function body_meta:DrawOutline( r, ... )
-	assert( self:IsValid() )
-	return DrawBodyOutline( self.handle, r, ... )
-end
-
---- Draws a highlight of the body.
----
----@param amount number
-function body_meta:DrawHighlight( amount )
-	assert( self:IsValid() )
-	return DrawBodyHighlight( self.handle, amount )
-end
-
---- Sets the transform of the body.
----
----@param tr Transformation
-function body_meta:SetTransform( tr )
-	assert( self:IsValid() )
-	return SetBodyTransform( self.handle, tr )
-end
-
---- Sets if the body should be simulated.
----
----@param bool boolean
-function body_meta:SetActive( bool )
-	assert( self:IsValid() )
-	return SetBodyActive( self.handle, bool )
-end
-
---- Sets if the body should move.
----
----@param bool boolean
-function body_meta:SetDynamic( bool )
-	assert( self:IsValid() )
-	return SetBodyDynamic( self.handle, bool )
-end
-
---- Sets the velocity of the body.
----
----@param vel Vector
-function body_meta:SetVelocity( vel )
-	assert( self:IsValid() )
-	return SetBodyVelocity( self.handle, vel )
-end
-
---- Sets the angular velocity of the body.
----
----@param avel Vector
-function body_meta:SetAngularVelocity( avel )
-	assert( self:IsValid() )
-	return SetBodyAngularVelocity( self.handle, avel )
-end
-
---- Gets the transform of the body.
----
----@return Transformation
-function body_meta:GetTransform()
-	assert( self:IsValid() )
-	return MakeTransformation( GetBodyTransform( self.handle ) )
-end
-
---- Gets the mass of the body.
----
----@return number
-function body_meta:GetMass()
-	assert( self:IsValid() )
-	return GetBodyMass( self.handle )
-end
-
---- Gets the velocity of the body.
----
----@return Vector
-function body_meta:GetVelocity()
-	assert( self:IsValid() )
-	return MakeVector( GetBodyVelocity( self.handle ) )
-end
-
---- Gets the velocity at the position on the body.
----
----@param pos Vector
----@return Vector
-function body_meta:GetVelocityAtPos( pos )
-	assert( self:IsValid() )
-	return MakeVector( GetBodyVelocityAtPos( self.handle, pos ) )
-end
-
---- Gets the angular velocity of the body.
----
----@return Vector
-function body_meta:GetAngularVelocity()
-	assert( self:IsValid() )
-	return MakeVector( GetBodyAngularVelocity( self.handle ) )
-end
-
---- Gets the shape of the body.
----
----@return Shape[]
-function body_meta:GetShapes()
-	assert( self:IsValid() )
-	local shapes = GetBodyShapes( self.handle )
-	for i = 1, #shapes do
-		shapes[i] = Shape( shapes[i] )
-	end
-	return shapes
-end
-
---- Gets the vehicle of the body.
----
----@return Vehicle?
-function body_meta:GetVehicle()
-	assert( self:IsValid() )
-	return Vehicle( GetBodyVehicle( self.handle ) )
-end
-
---- Gets the bounds of the body.
----
----@return Vector min
----@return Vector max
-function body_meta:GetWorldBounds()
-	assert( self:IsValid() )
-	local min, max = GetBodyBounds( self.handle )
-	return MakeVector( min ), MakeVector( max )
-end
-
---- Gets the center of mas in object-space.
----
----@return Vector
-function body_meta:GetLocalCenterOfMass()
-	assert( self:IsValid() )
-	return MakeVector( GetBodyCenterOfMass( self.handle ) )
-end
-
---- Gets the center of mass in world-space.
----
----@return Vector
-function body_meta:GetWorldCenterOfMass()
-	return self:GetTransform():ToGlobal( self:GetLocalCenterOfMass() )
-end
-
---- Gets the closest point to the body from a given origin.
----
----@param origin Vector
----@return boolean hit
----@return Vector point
----@return Vector normal
----@return Shape shape
-function body_meta:GetClosestPoint( origin )
-	local hit, point, normal, shape = GetBodyClosestPoint( self.handle, origin )
-	if not hit then
-		return false
-	end
-	return hit, MakeVector( point ), MakeVector( normal ), Shape( shape )
-end
-
---- Gets all the dynamic bodies in the jointed structure.
---- The result will include the current body.
----
----@return Body[] jointed
-function body_meta:GetJointedBodies()
-	local list = GetJointedBodies( self.handle )
-	for i = 1, #list do
-		list[i] = Body( list[i] )
-	end
-	return list
-end
-
---- Gets if the body is currently being simulated.
----
----@return boolean
-function body_meta:IsActive()
-	assert( self:IsValid() )
-	return IsBodyActive( self.handle )
-end
-
---- Gets if the body is dynamic.
----
----@return boolean
-function body_meta:IsDynamic()
-	assert( self:IsValid() )
-	return IsBodyDynamic( self.handle )
-end
-
---- Gets if the body is visble on screen.
----
----@param maxdist number
----@return boolean
-function body_meta:IsVisible( maxdist )
-	assert( self:IsValid() )
-	return IsBodyVisible( self.handle, maxdist )
-end
-
---- Gets if the body has been broken.
----
----@return boolean
-function body_meta:IsBroken()
-	return not self:IsValid() or IsBodyBroken( self.handle )
-end
-
---- Gets if the body somehow attached to something static.
----
----@return boolean
-function body_meta:IsJointedToStatic()
-	assert( self:IsValid() )
-	return IsBodyJointedToStatic( self.handle )
-end
-
- end)();
---src/entities/joint.lua
-(function() ----------------
--- Joint class and related functions
--- @script entities.joint
-
----@class Joint: Entity
-local joint_meta
-joint_meta = global_metatable( "joint", "entity" )
-
---- Tests if the parameter is a joint entity.
----
----@param e any
----@return boolean
-function IsJoint( e )
-	return IsEntity( e ) and e.type == "joint"
-end
-
---- Wraps the given handle with the joint class.
----
----@param handle number
----@return Joint?
-function Joint( handle )
-	if handle > 0 then
-		return setmetatable( { handle = handle, type = "joint" }, joint_meta )
-	end
-end
-
---- Finds a joint with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Joint?
-function FindJointByTag( tag, global )
-	return Joint( FindJoint( tag, global ) )
-end
-
---- Finds all joints with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Joint[]
-function FindJointsByTag( tag, global )
-	local t = FindJoints( tag, global )
-	for i = 1, #t do
-		t[i] = Joint( t[i] )
-	end
-	return t
-end
-
----@type Joint
-
----@return string
-function joint_meta:__tostring()
-	return string.format( "Joint[%d]", self.handle )
-end
-
---- Detatches the joint from the given shape.
----
----@param shape Shape
-function joint_meta:DetachFromShape( shape )
-	DetachJointFromShape( self.handle, GetEntityHandle( shape ) )
-end
-
---- Makes the joint behave as a motor.
----
----@param velocity number
----@param strength number
-function joint_meta:SetMotor( velocity, strength )
-	assert( self:IsValid() )
-	return SetJointMotor( self.handle, velocity, strength )
-end
-
---- Makes the joint behave as a motor moving to the specified target.
----
----@param target number
----@param maxVel number
----@param strength number
-function joint_meta:SetMotorTarget( target, maxVel, strength )
-	assert( self:IsValid() )
-	return SetJointMotorTarget( self.handle, target, maxVel, strength )
-end
-
---- Gets the type of the joint.
----
----@return string
-function joint_meta:GetJointType()
-	assert( self:IsValid() )
-	return GetJointType( self.handle )
-end
-
---- Finds the other shape the joint is attached to.
----
----@param shape Shape | number
----@return Shape
-function joint_meta:GetOtherShape( shape )
-	assert( self:IsValid() )
-	return Shape( GetJointOtherShape( self.handle, GetEntityHandle( shape ) ) )
-end
-
---- Gets the limits of the joint.
----
----@return number min
----@return number max
-function joint_meta:GetLimits()
-	assert( self:IsValid() )
-	return GetJointLimits( self.handle )
-end
-
---- Gets the current position or angle of the joint.
----
----@return number
-function joint_meta:GetMovement()
-	assert( self:IsValid() )
-	return GetJointMovement( self.handle )
-end
-
---- Gets if the joint is broken.
----
----@return boolean
-function joint_meta:IsBroken()
-	return not self:IsValid() or IsJointBroken( self.handle )
-end
-
-
- end)();
---src/entities/light.lua
-(function() ----------------
--- Light class and related functions
--- @script entities.light
-
----@class Light: Entity
-local light_meta
-light_meta = global_metatable( "light", "entity" )
-
---- Tests if the parameter is a light entity.
----
----@param e any
----@return boolean
-function IsLight( e )
-	return IsEntity( e ) and e.type == "light"
-end
-
---- Wraps the given handle with the light class.
----
----@param handle number
----@return Light?
-function Light( handle )
-	if handle > 0 then
-		return setmetatable( { handle = handle, type = "light" }, light_meta )
-	end
-end
-
---- Finds a light with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Light?
-function FindLightByTag( tag, global )
-	return Light( FindLight( tag, global ) )
-end
-
---- Finds all lights with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Light[]
-function FindLightsByTag( tag, global )
-	local t = FindLights( tag, global )
-	for i = 1, #t do
-		t[i] = Light( t[i] )
-	end
-	return t
-end
-
----@type Light
-
----@return string
-function light_meta:__tostring()
-	return string.format( "Light[%d]", self.handle )
-end
-
---- Sets if the light is enabled.
----
----@param enabled boolean
-function light_meta:SetEnabled( enabled )
-	assert( self:IsValid() )
-	return SetLightEnabled( self.handle, enabled )
-end
-
---- Sets the color of the light.
----
----@param r number
----@param g number
----@param b number
-function light_meta:SetColor( r, g, b )
-	assert( self:IsValid() )
-	return SetLightColor( self.handle, r, g, b )
-end
-
---- Sets the intensity of the light.
----
----@param intensity number
-function light_meta:SetIntensity( intensity )
-	assert( self:IsValid() )
-	return SetLightIntensity( self.handle, intensity )
-end
-
---- Gets the transform of the light.
----
----@return Transformation
-function light_meta:GetTransform()
-	assert( self:IsValid() )
-	return MakeTransformation( GetLightTransform( self.handle ) )
-end
-
---- Gets the shape the light is attached to.
----
----@return Shape
-function light_meta:GetShape()
-	assert( self:IsValid() )
-	return Shape( GetLightShape( self.handle ) )
-end
-
---- Gets if the light is active.
----
----@return boolean
-function light_meta:IsActive()
-	assert( self:IsValid() )
-	return IsLightActive( self.handle )
-end
-
---- Gets if the specified point is affected by the light.
----
----@param point Vector
----@return boolean
-function light_meta:IsPointAffectedByLight( point )
-	assert( self:IsValid() )
-	return IsPointAffectedByLight( self.handle, point )
-end
-
- end)();
---src/entities/location.lua
-(function() ----------------
--- Location class and related functions
--- @script entities.location
-
----@class Location: Entity
-local location_meta
-location_meta = global_metatable( "location", "entity" )
-
---- Tests if the parameter is a location entity.
----
----@param e any
----@return boolean
-function IsLocation( e )
-	return IsEntity( e ) and e.type == "location"
-end
-
---- Wraps the given handle with the location class.
----
----@param handle number
----@return Location?
-function Location( handle )
-	if handle > 0 then
-		return setmetatable( { handle = handle, type = "location" }, location_meta )
-	end
-end
-
---- Finds a location with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Location?
-function FindLocationByTag( tag, global )
-	return Location( FindLocation( tag, global ) )
-end
-
---- Finds all locations with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Location[]
-function FindLocationsByTag( tag, global )
-	local t = FindLocations( tag, global )
-	for i = 1, #t do
-		t[i] = Location( t[i] )
-	end
-	return t
-end
-
----@type Location
-
----@return string
-function location_meta:__tostring()
-	return string.format( "Location[%d]", self.handle )
-end
-
---- Gets the transform of the location.
----
----@return Transformation
-function location_meta:GetTransform()
-	assert( self:IsValid() )
-	return MakeTransformation( GetLocationTransform( self.handle ) )
-end
-
- end)();
---src/entities/player.lua
-(function() ----------------
--- Player class and related functions
--- @script entities.player
-
----@class Player
-local player_meta
-player_meta = global_metatable( "player" )
-
----@type Player
-PLAYER = setmetatable( {}, player_meta )
-
----@param data string
----@return Player self
-function player_meta:__unserialize( data )
-	return self
-end
-
----@return string data
-function player_meta:__serialize()
-	return ""
-end
-
----@return string
-function player_meta:__tostring()
-	return string.format( "Player" )
-end
-
---- Gets the type of the entity.
----
----@return string type
-function player_meta:GetType()
-	return "player"
-end
-
---- Repawns the player.
-function player_meta:Respawn()
-	return RespawnPlayer()
-end
-
---- Release what the player is currently holding.
----
-function player_meta:ReleaseGrab()
-	ReleasePlayerGrab()
-end
-
---- Sets the transform of the player.
----
----@param transform Transformation
-function player_meta:SetTransform( transform )
-	return SetPlayerTransform( transform )
-end
-
---- Sets the transform of the camera.
----
----@param transform Transformation
-function player_meta:SetCamera( transform )
-	return SetCameraTransform( transform )
-end
-
---- Sets the Field of View of the camera.
----
----@param degrees number
-function player_meta:SetFov( degrees )
-	return SetCameraFov( degrees )
-end
-
---- Sets the Depth of Field of the camera.
----
----@param distance number
----@param amount number
-function player_meta:SetDof( distance, amount )
-	return SetCameraDof( distance, amount )
-end
-
---- Sets the transform of the player spawn.
----
----@param transform Transformation
-function player_meta:SetSpawnTransform( transform )
-	return SetPlayerSpawnTransform( transform )
-end
-
---- Sets the vehicle the player is currently riding.
----
----@param handle Vehicle | number
-function player_meta:SetVehicle( handle )
-	return SetPlayerVehicle( GetEntityHandle( handle ) )
-end
-
---- Sets the velocity of the player.
----
----@param velocity Vector
-function player_meta:SetVelocity( velocity )
-	return SetPlayerVelocity( velocity )
-end
-
---- Sets the screen the player is currently viewing.
----
----@param handle Screen | number
-function player_meta:SetScreen( handle )
-	return SetPlayerScreen( GetEntityHandle( handle ) )
-end
-
---- Sets the health of the player.
----
----@param health number
-function player_meta:SetHealth( health )
-	return SetPlayerHealth( health )
-end
-
---- Sets the velocity of the ground for the player,
---- Effectively turning it into a conveyor belt of sorts.
----
----@param vel Vector
-function player_meta:SetGroundVelocity(vel)
-	SetPlayerGroundVelocity(vel)
-end
-
---- Gets the transform of the player.
----
----@return Transformation
-function player_meta:GetTransform()
-	return MakeTransformation( GetPlayerTransform() )
-end
-
---- Gets the transform of the player camera.
----
----@return Transformation
-function player_meta:GetPlayerCamera()
-	return MakeTransformation( GetPlayerCameraTransform() )
-end
-
---- Gets the transform of the camera.
----
----@return Transformation
-function player_meta:GetCamera()
-	return MakeTransformation( GetCameraTransform() )
-end
-
---- Gets the velocity of the player.
----
----@return Vector
-function player_meta:GetVelocity()
-	return MakeVector( GetPlayerVelocity() )
-end
-
---- Gets the vehicle the player is currently riding.
----
----@return Vehicle
-function player_meta:GetVehicle()
-	return Vehicle( GetPlayerVehicle() )
-end
-
---- Gets the shape the player is currently grabbing.
----
----@return Shape
-function player_meta:GetGrabShape()
-	return Shape( GetPlayerGrabShape() )
-end
-
---- Gets the body the player is currently grabbing.
----
----@return Body
-function player_meta:GetGrabBody()
-	return Body( GetPlayerGrabBody() )
-end
-
---- Gets the pick-able shape the player is currently targetting.
----
----@return Shape
-function player_meta:GetPickShape()
-	return Shape( GetPlayerPickShape() )
-end
-
---- Gets the pick-able body the player is currently targetting.
----
----@return Body
-function player_meta:GetPickBody()
-	return Body( GetPlayerPickBody() )
-end
-
---- Gets the interactible shape the player is currently targetting.
----
----@return Shape
-function player_meta:GetInteractShape()
-	return Shape( GetPlayerInteractShape() )
-end
-
---- Gets the interactible body the player is currently targetting.
----
----@return Body
-function player_meta:GetInteractBody()
-	return Body( GetPlayerInteractBody() )
-end
-
---- Gets the screen the player is currently interacting with.
----
----@return Screen
-function player_meta:GetScreen()
-	return Screen( GetPlayerScreen() )
-end
-
---- Gets the player health.
----
----@return number
-function player_meta:GetHealth()
-	return GetPlayerHealth()
-end
-
- end)();
---src/entities/screen.lua
-(function() ----------------
--- Screen class and related functions
--- @script entities.screen
-
----@class Screen: Entity
-local screen_meta
-screen_meta = global_metatable( "screen", "entity" )
-
---- Tests if the parameter is a screen entity.
----
----@param e any
----@return boolean
-function IsScreen( e )
-	return IsEntity( e ) and e.type == "screen"
-end
-
---- Wraps the given handle with the screen class.
----
----@param handle number
----@return Screen?
-function Screen( handle )
-	if handle > 0 then
-		return setmetatable( { handle = handle, type = "screen" }, screen_meta )
-	end
-end
-
---- Finds a screen with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Screen?
-function FindScreenByTag( tag, global )
-	return Screen( FindScreen( tag, global ) )
-end
-
---- Finds all screens with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Screen[]
-function FindScreensByTag( tag, global )
-	local t = FindScreens( tag, global )
-	for i = 1, #t do
-		t[i] = Screen( t[i] )
-	end
-	return t
-end
-
----@type Screen
-
----@return string
-function screen_meta:__tostring()
-	return string.format( "Screen[%d]", self.handle )
-end
-
---- Sets if the screen is enabled.
----
----@param enabled boolean
-function screen_meta:SetEnabled( enabled )
-	assert( self:IsValid() )
-	return SetScreenEnabled( self.handle, enabled )
-end
-
---- Gets the shape the screen is attached to.
----
----@return Shape
-function screen_meta:GetShape()
-	assert( self:IsValid() )
-	return Shape( GetScreenShape( self.handle ) )
-end
-
---- Gets if the screen is enabled.
----
----@return boolean
-function screen_meta:IsEnabled()
-	assert( self:IsValid() )
-	return IsScreenEnabled( self.handle )
-end
-
- end)();
---src/entities/shape.lua
-(function() ----------------
--- Shape class and related functions
--- @script entities.shape
-
----@class Shape: Entity
-local shape_meta
-shape_meta = global_metatable( "shape", "entity" )
-
---- Tests if the parameter is a shape entity.
----
----@param e any
----@return boolean
-function IsShape( e )
-	return IsEntity( e ) and e.type == "shape"
-end
-
---- Wraps the given handle with the shape class.
----
----@param handle number
----@return Shape?
-function Shape( handle )
-	if handle > 0 then
-		return setmetatable( { handle = handle, type = "shape" }, shape_meta )
-	end
-end
-
---- Finds a shape with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Shape?
-function FindShapeByTag( tag, global )
-	return Shape( FindShape( tag, global ) )
-end
-
---- Finds all shapes with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Shape[]
-function FindShapesByTag( tag, global )
-	local t = FindShapes( tag, global )
-	for i = 1, #t do
-		t[i] = Shape( t[i] )
-	end
-	return t
-end
-
----@type Shape
-
----@return string
-function shape_meta:__tostring()
-	return string.format( "Shape[%d]", self.handle )
-end
-
---- Draws the outline of the shape.
----
----@param r number
----@overload fun(r: number, g: number, b: number, a: number)
-function shape_meta:DrawOutline( r, ... )
-	assert( self:IsValid() )
-	return DrawShapeOutline( self.handle, r, ... )
-end
-
---- Draws a highlight of the shape.
----
----@param amount number
-function shape_meta:DrawHighlight( amount )
-	assert( self:IsValid() )
-	return DrawShapeHighlight( self.handle, amount )
-end
-
---- Sets the transform of the shape relative to its body.
----
----@param transform Transformation
-function shape_meta:SetLocalTransform( transform )
-	assert( self:IsValid() )
-	return SetShapeLocalTransform( self.handle, transform )
-end
-
---- Sets the emmissivity scale of the shape.
----
----@param scale number
-function shape_meta:SetEmissiveScale( scale )
-	assert( self:IsValid() )
-	return SetShapeEmissiveScale( self.handle, scale )
-end
-
---- Sets the collision filter of the shape.
---- A shape will only collide with another if the following is true:
---- ```
---- (A.layer & B.mask) && (B.layer & A.mask)
---- ```
----
----@param layer? number bit array (8 bits, 0-255)
----@param mask? number bit mask (8 bits, 0-255)
-function shape_meta:SetCollisionFilter( layer, mask )
-	SetShapeCollisionFilter( self.handle, layer or 1, mask or 255 )
-end
-
---- Gets the transform of the shape relative to its body.
----
----@return Transformation
-function shape_meta:GetLocalTransform()
-	assert( self:IsValid() )
-	return MakeTransformation( GetShapeLocalTransform( self.handle ) )
-end
-
---- Gets the transform of the shape.
----
----@return Transformation
-function shape_meta:GetWorldTransform()
-	assert( self:IsValid() )
-	return MakeTransformation( GetShapeWorldTransform( self.handle ) )
-end
-
---- Gets the body of this shape.
----
----@return Body
-function shape_meta:GetBody()
-	assert( self:IsValid() )
-	return Body( GetShapeBody( self.handle ) )
-end
-
---- Gets the joints attached to this shape.
----
----@return Joint[]
-function shape_meta:GetJoints()
-	assert( self:IsValid() )
-	local joints = GetShapeJoints( self.handle )
-	for i = 1, #joints do
-		joints[i] = Joint( joints[i] )
-	end
-	return joints
-end
-
---- Gets the lights attached to this shape.
----
----@return Light[]
-function shape_meta:GetLights()
-	assert( self:IsValid() )
-	local lights = GetShapeLights( self.handle )
-	for i = 1, #lights do
-		lights[i] = Light( lights[i] )
-	end
-	return lights
-end
-
---- Gets the bounds of the shape.
----
----@return Vector min
----@return Vector max
-function shape_meta:GetWorldBounds()
-	assert( self:IsValid() )
-	local min, max = GetShapeBounds( self.handle )
-	return MakeVector( min ), MakeVector( max )
-end
-
---- Gets the material and color of the shape at the specified position.
----
----@param pos Vector
----@return string type
----@return number r
----@return number g
----@return number b
----@return number a
-function shape_meta:GetMaterialAtPos( pos )
-	assert( self:IsValid() )
-	return GetShapeMaterialAtPosition( self.handle, pos )
-end
-
---- Gets the size of the shape in voxels.
----
----@return number x
----@return number y
----@return number z
-function shape_meta:GetSize()
-	assert( self:IsValid() )
-	return GetShapeSize( self.handle )
-end
-
---- Gets the count of voxels in the shape.
----
----@return number
-function shape_meta:GetVoxelCount()
-	assert( self:IsValid() )
-	return GetShapeVoxelCount( self.handle )
-end
-
---- Gets the closest point to the shape from a given origin.
----
----@param origin Vector
----@return boolean hit
----@return Vector point
----@return Vector normal
-function shape_meta:GetClosestPoint( origin )
-	local hit, point, normal = GetShapeClosestPoint( self.handle, origin )
-	if not hit then
-		return false
-	end
-	return hit, MakeVector( point ), MakeVector( normal )
-end
-
---- Gets if the shape is currently visible.
----
----@param maxDist number
----@param rejectTransparent? boolean
----@return boolean
-function shape_meta:IsVisible( maxDist, rejectTransparent )
-	assert( self:IsValid() )
-	return IsShapeVisible( self.handle, maxDist, rejectTransparent )
-end
-
---- Gets if the shape has been broken.
----
----@return boolean
-function shape_meta:IsBroken()
-	return not self:IsValid() or IsShapeBroken( self.handle )
-end
-
- end)();
---src/entities/trigger.lua
-(function() ----------------
--- Trigger class and related functions
--- @script entities.trigger
-
----@class Trigger: Entity
-local trigger_meta
-trigger_meta = global_metatable( "trigger", "entity" )
-
---- Tests if the parameter is a trigger entity.
----
----@param e any
----@return boolean
-function IsTrigger( e )
-	return IsEntity( e ) and e.type == "trigger"
-end
-
---- Wraps the given handle with the trigger class.
----
----@param handle number
----@return Trigger?
-function Trigger( handle )
-	if handle > 0 then
-		return setmetatable( { handle = handle, type = "trigger" }, trigger_meta )
-	end
-end
-
---- Finds a trigger with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Trigger?
-function FindTriggerByTag( tag, global )
-	return Trigger( FindTrigger( tag, global ) )
-end
-
---- Finds all triggers with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Trigger[]
-function FindTriggersByTag( tag, global )
-	local t = FindTriggers( tag, global )
-	for i = 1, #t do
-		t[i] = Trigger( t[i] )
-	end
-	return t
-end
-
----@type Trigger
-
----@return string
-function trigger_meta:__tostring()
-	return string.format( "Trigger[%d]", self.handle )
-end
-
---- Sets the transform of the trigger.
----
----@param transform Transformation
-function trigger_meta:SetTransform( transform )
-	assert( self:IsValid() )
-	return SetTriggerTransform( self.handle, transform )
-end
-
---- Gets the transform of the trigger.
----
----@return Transformation
-function trigger_meta:GetTransform()
-	assert( self:IsValid() )
-	return MakeTransformation( GetTriggerTransform( self.handle ) )
-end
-
---- Gets the distance to the trigger from a given origin.
---- Negative values indicate the origin is inside the trigger.
----
----@param origin Vector
-function trigger_meta:GetDistance(origin)
-	return GetTriggerDistance(self.handle, origin)
-end
-
---- Gets the closest point to the trigger from a given origin.
----
----@param origin Vector
-function trigger_meta:GetClosestPoint(origin)
-	return MakeVector(GetTriggerDistance(self.handle, origin))
-end
-
---- Gets the bounds of the trigger.
----
----@return Vector min
----@return Vector max
-function trigger_meta:GetWorldBounds()
-	assert( self:IsValid() )
-	local min, max = GetTriggerBounds( self.handle )
-	return MakeVector( min ), MakeVector( max )
-end
-
---- Gets if the specified body is in the trigger.
----
----@param handle Body | number
----@return boolean
-function trigger_meta:IsBodyInTrigger( handle )
-	assert( self:IsValid() )
-	return IsBodyInTrigger( self.handle, GetEntityHandle( handle ) )
-end
-
---- Gets if the specified vehicle is in the trigger.
----
----@param handle Vehicle | number
----@return boolean
-function trigger_meta:IsVehicleInTrigger( handle )
-	assert( self:IsValid() )
-	return IsVehicleInTrigger( self.handle, GetEntityHandle( handle ) )
-end
-
---- Gets if the specified shape is in the trigger.
----
----@param handle Shape | number
----@return boolean
-function trigger_meta:IsShapeInTrigger( handle )
-	assert( self:IsValid() )
-	return IsShapeInTrigger( self.handle, GetEntityHandle( handle ) )
-end
-
---- Gets if the specified point is in the trigger.
----
----@param point Vector
----@return boolean
-function trigger_meta:IsPointInTrigger( point )
-	assert( self:IsValid() )
-	return IsPointInTrigger( self.handle, point )
-end
-
---- Gets if the trigger is empty.
----
----@param demolision boolean
----@return boolean empty
----@return Vector? highpoint
-function trigger_meta:IsEmpty( demolision )
-	assert( self:IsValid() )
-	local empty, highpoint = IsTriggerEmpty( self.handle, demolision )
-	return empty, highpoint and MakeVector( highpoint )
-end
-
- end)();
---src/entities/vehicle.lua
-(function() ----------------
--- Vehicle class and related functions
--- @script entities.vehicle
-
----@class Vehicle: Entity
-local vehicle_meta
-vehicle_meta = global_metatable( "vehicle", "entity" )
-
---- Tests if the parameter is a vehicle entity.
----
----@param e any
----@return boolean
-function IsVehicle( e )
-	return IsEntity( e ) and e.type == "vehicle"
-end
-
---- Wraps the given handle with the vehicle class.
----
----@param handle number
----@return Vehicle?
-function Vehicle( handle )
-	if handle > 0 then
-		return setmetatable( { handle = handle, type = "vehicle" }, vehicle_meta )
-	end
-end
-
---- Finds a vehicle with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Vehicle?
-function FindVehicleByTag( tag, global )
-	return Vehicle( FindVehicle( tag, global ) )
-end
-
---- Finds all vehicles with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Vehicle[]
-function FindVehiclesByTag( tag, global )
-	local t = FindVehicles( tag, global )
-	for i = 1, #t do
-		t[i] = Vehicle( t[i] )
-	end
-	return t
-end
-
----@type Vehicle
-
----@return string
-function vehicle_meta:__tostring()
-	return string.format( "Vehicle[%d]", self.handle )
-end
-
---- Drives the vehicle by setting its controls.
----
----@param drive number
----@param steering number
----@param handbrake number
-function vehicle_meta:Drive( drive, steering, handbrake )
-	assert( self:IsValid() )
-	return DriveVehicle( self.handle, drive, steering, handbrake )
-end
-
---- Gets the transform of the vehicle.
----
----@return Transformation
-function vehicle_meta:GetTransform()
-	assert( self:IsValid() )
-	return MakeTransformation( GetVehicleTransform( self.handle ) )
-end
-
---- Gets the body of the vehicle.
----
----@return Body
-function vehicle_meta:GetBody()
-	assert( self:IsValid() )
-	return Body( GetVehicleBody( self.handle ) )
-end
-
---- Gets the health of the vehicle.
----
----@return number
-function vehicle_meta:GetHealth()
-	assert( self:IsValid() )
-	-- TODO: calculate ourselves if we need to
-	return GetVehicleHealth( self.handle )
-end
-
---- Gets the position of the driver camera in object-space.
----
----@return Vector
-function vehicle_meta:GetDriverPos()
-	assert( self:IsValid() )
-	return MakeVector( GetVehicleDriverPos( self.handle ) )
-end
-
---- Gets the position of the driver camera in world-space.
----
----@return Vector
-function vehicle_meta:GetGlobalDriverPos()
-	return self:GetTransform():ToGlobal( self:GetDriverPos() )
-end
-
- end)();
---src/animation/animation.lua
-(function() 
-local animator_meta = global_metatable( "animator" )
-
-function animator_meta:Update( dt )
-	self.value = self._func( self._state, self._modifier * dt ) or self._state.value or 0
-	return self.value
-end
-
-function animator_meta:Reset()
-	self._state = {}
-	if self._init then
-		self._init( self._state )
-	end
-	self.value = self._state.value or 0
-end
-
-function animator_meta:SetModifier( num )
-	self._modifier = num
-end
-
-function animator_meta:__newindex( k, v )
-	self._state[k] = v
-end
-
-function animator_meta:__index( k )
-	local v = animator_meta[k]
-	if v then
-		return v
-	end
-	return rawget( self, "_state" )[k]
-end
-
-Animator = {
-	Base = function( easing )
-		local t = setmetatable( {
-			_state = {},
-			_func = type( easing ) == "table" and easing.update or easing,
-			_init = type( easing ) == "table" and easing.init,
-			_modifier = 1,
-			value = 0,
-		}, animator_meta )
-		if t._init then
-			t._init( t._state )
-		end
-		return t
-	end,
-}
-
-Animator.LinearApproach = function( init, speed, down_speed )
-	return Animator.Base {
-		update = function( state, dt )
-			if state.target < state.value then
-				state.value = state.value + math.max( state.target - state.value, dt * state.down_speed )
-			elseif state.target > state.value then
-				state.value = state.value + math.min( state.target - state.value, dt * state.speed )
-			end
-		end,
-		init = function( state )
-			state.value = init
-			state.speed = speed
-			state.down_speed = down_speed or -speed
-			state.target = init
-		end,
-	}
-end
-
-Animator.SpeedLinearApproach = function( init, acceleration, down_acceleration )
-	return Animator.Base {
-		update = function( state, dt )
-			state.driver.target = state.target
-			state.driver.speed = state.acceleration
-			state.driver.down_speed = state.down_acceleration
-			state.value = state.value + state.driver:Update( dt ) * dt
-		end,
-		init = function( state )
-			state.driver = Animator.LinearApproach( init, acceleration )
-			state.target = init
-			state.acceleration = acceleration
-			state.down_acceleration = down_acceleration
-			state.value = 0
-		end,
-	}
-end
-
- end)();
---src/animation/armature.lua
-(function() ----------------
--- Armature library
--- @script animation.armature
-
----@class Armature
----@field refs any
----@field root any
----@field scale number | nil
----@field dirty boolean
-local armature_meta
-armature_meta = global_metatable( "armature" )
-
---[[
-
-Armature {
-    shapes = {
-        "core_2",
-        "core_1",
-        "core_0",
-        "arm_21",
-        "arm_11",
-        "arm_01",
-        "arm_20",
-        "arm_10",
-        "arm_00",
-        "body"
-    },
-
-    bones = {
-        name = "root",
-        shapes = {
-            body = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-        },
-        {
-            name = "core_0",
-            shapes = {
-                core_0 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-            },
-        },
-        {
-            name = "core_1",
-            shapes = {
-                core_1 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-            },
-        },
-        {
-            name = "core_2",
-            shapes = {
-                core_2 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-            },
-        },
-        {
-            name = "arm_00",
-            shapes = {
-                arm_00 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-            },
-            {
-                name = "arm_01",
-                shapes = {
-                    arm_01 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-                },
-            },
-        },
-        {
-            name = "arm_10",
-            shapes = {
-                arm_10 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-            },
-            {
-                name = "arm_11",
-                shapes = {
-                    arm_11 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-                },
-            },
-        },
-        {
-            name = "arm_20",
-            shapes = {
-                arm_20 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-            },
-            {
-                name = "arm_21",
-                shapes = {
-                    arm_21 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-                },
-            },
-        },
-    }
-}
-
-]]
-
---- Loads armature information from a prefab and a list of shapes.
----
----@param xml string
----@param parts table[]
----@param scale? number
-function LoadArmatureFromXML( xml, parts, scale ) -- Example below
-	scale = scale or 1
-	local dt = ParseXML( xml )
-	assert( (dt.type == "prefab" and dt.children[1] and dt.children[1].type == "group") or dt.type == "group", "Invalid Tool XML" )
-	local shapes = {}
-	local offsets = {}
-	for i = 1, #parts do
-		shapes[i] = parts[i][1]
-		local v = parts[i][2]
-		-- Compensate for the editor placing vox parts relative to the center of the base
-		offsets[parts[i][1]] = Vec( math.floor( v[1] / 2 ) / 10, 0, -math.floor( v[2] / 2 ) / 10 )
-	end
-
-	local function parseVec( str )
-		if not str then
-			return Vec( 0, 0, 0 )
-		end
-		local x, y, z = str:match( "([%d.-]+) ([%d.-]+) ([%d.-]+)" )
-		return Vec( tonumber( x ), tonumber( y ), tonumber( z ) )
-	end
-
-	local function parseTransform( attr )
-		local pos, angv = parseVec( attr.pos ), parseVec( attr.rot )
-		return Transform( Vec( pos[1], pos[2], pos[3] ), QuatEuler( angv[1], angv[2], angv[3] ) )
-	end
-
-	local function translatebone( node, isLocation )
-		local t = { name = node.attributes.name, transform = parseTransform( node.attributes ) }
-		local sub = t
-		if not isLocation then
-			t.name = "__FIXED_" .. node.attributes.name
-			t[1] = { name = node.attributes.name }
-			sub = t[1]
-		end
-		sub.shapes = {}
-		for i = 1, #node.children do
-			local child = node.children[i]
-			if child.type == "vox" then
-				local name = child.attributes.object
-				local tr = parseTransform( child.attributes )
-				local s = child.attributes.scale and tonumber( child.attributes.scale ) or 1
-				tr.pos = VecSub( tr.pos, VecScale( offsets[name], s ) )
-				tr.rot = QuatRotateQuat( tr.rot, QuatEuler( -90, 0, 0 ) )
-				sub.shapes[name] = tr
-			elseif child.type == "group" then
-				sub[#sub + 1] = translatebone( child )
-			elseif child.type == "location" then
-				sub[#sub + 1] = translatebone( child, true )
-			end
-		end
-		return t
-	end
-	local bones = translatebone( dt.type == "prefab" and dt.children[1] or dt )[1]
-	bones.transform = Transform( Vec(), QuatEuler( 0, 0, 0 ) )
-	bones.name = "root"
-
-	local arm = Armature { shapes = shapes, scale = scale, bones = bones }
-	arm:ComputeBones()
-	return arm, dt
-end
---[=[
---[[---------------------------------------------------
-    LoadArmatureFromXML is capable of taking the XML of a prefab and turning it into a useable armature object for tools and such.
-    Two things are required: the XML of the prefab itself, and a list of all the objects inside the vox for position correction.
-    The list of objects should be as it appears in MagicaVoxel, with every slot corresponding to an object in the vox file.
-    One notable limitation is that there can only be one vox file used and that all the objects inside it can only be used once.
---]]---------------------------------------------------
-
--- Loading the armature from the prefab and the objects list
-local armature = LoadArmatureFromXML([[
-<prefab version="0.7.0">
-    <group open_="true" name="instance=MOD/physgun.xml" pos="-3.4 0.7 0.0">
-        <vox pos="-0.125 -0.125 0.125" file="MOD/physgun.vox" object="body" scale="0.5"/>
-        <group open_="true" name="core0" pos="0.0 0.0 -0.075">
-            <vox pos="-0.025 -0.125 0.0" file="MOD/physgun.vox" object="core_0" scale="0.5"/>
-        </group>
-        <group open_="true" name="core1" pos="0.0 0.0 -0.175">
-            <vox pos="-0.025 -0.125 0.0" file="MOD/physgun.vox" object="core_1" scale="0.5"/>
-        </group>
-        <group open_="true" name="core2" pos="0.0 0.0 -0.275">
-            <vox pos="-0.025 -0.125 0.0" file="MOD/physgun.vox" object="core_2" scale="0.5"/>
-        </group>
-        <group open_="true" name="arms_rot" pos="0.0 0.0 -0.375">
-            <group open_="true" name="arm0_base" pos="0.0 0.1 0.0">
-                <vox pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_00" scale="0.5"/>
-                <group open_="true" name="arm0_tip" pos="0.0 0.2 -0.0">
-                    <vox pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_01" scale="0.5"/>
-                </group>
-            </group>
-            <group open_="true" name="arm1_base" pos="0.087 -0.05 0.0" rot="180.0 180.0 -60.0">
-                <vox pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_10" scale="0.5"/>
-                <group open_="true" name="arm1_tip" pos="0.0 0.2 0.0">
-                    <vox pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_11" scale="0.5"/>
-                </group>
-            </group>
-            <group open_="true" name="arm2_base" pos="-0.087 -0.05 0.0" rot="180.0 180.0 60.0">
-                <vox pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_20" scale="0.5"/>
-                <group open_="true" name="arm2_tip" pos="0.0 0.2 0.0">
-                    <vox pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_21" scale="0.5"/>
-                </group>
-            </group>
-        </group>
-        <group open_="true" name="nozzle" pos="0.0 0.0 -0.475">
-            <vox pos="-0.025 -0.125 0.1" file="MOD/physgun.vox" object="cannon" scale="0.5"/>
-        </group>
-    </group>
-</prefab>
-]], {
-    -- The list of objects as it appears in MagicaVoxel. Each entry has the name of the object followed by the size as seen in MagicaVoxel.
-    -- Please note that the order MUST be the same as in MagicaVoxel and that there can be no gaps.
-    {"cannon", Vec(5, 3, 5)},
-    {"core_2", Vec(5, 2, 5)},
-    {"core_1", Vec(5, 2, 5)},
-    {"core_0", Vec(5, 2, 5)},
-    {"arm_21", Vec(1, 1, 2)},
-    {"arm_11", Vec(1, 1, 2)},
-    {"arm_01", Vec(1, 1, 2)},
-    {"arm_20", Vec(1, 1, 4)},
-    {"arm_10", Vec(1, 1, 4)},
-    {"arm_00", Vec(1, 1, 4)},
-    {"body", Vec(9, 6, 5)}
-})
------------------------------------------------------
-
--- Every frame you can animate the armature by setting the local transform of bones and then applying the changes to the shapes of the object.
-armature:SetBoneTransform("core0", Transform(Vec(), QuatEuler(0, 0, GetTime()*73)))
-armature:SetBoneTransform("core1", Transform(Vec(), QuatEuler(0, 0, -GetTime()*45)))
-armature:SetBoneTransform("core2", Transform(Vec(), QuatEuler(0, 0, GetTime()*83)))
-armature:SetBoneTransform("arms_rot", Transform(Vec(), QuatEuler(0, 0, GetTime()*20)))
-local tr = Transform(Vec(0,0,0), QuatEuler(-40 + 5 * math.sin(GetTime()), 0, 0))
-armature:SetBoneTransform("arm0_base", tr)
-armature:SetBoneTransform("arm0_tip", tr)
-armature:SetBoneTransform("arm1_base", tr)
-armature:SetBoneTransform("arm1_tip", tr)
-armature:SetBoneTransform("arm2_base", tr)
-armature:SetBoneTransform("arm2_tip", tr)
--- shapes is the list of all the shapes of the vox, it can be obtained with GetBodyShapes()
-armature:Apply(shapes)
-
---]=]
-
---- Creates a new armature.
----
----@param definition table
----@return Armature
-function Armature( definition )
-	local ids = {}
-	for i, name in ipairs( definition.shapes ) do
-		ids[name] = #definition.shapes - i + 1
-	end
-	local armature = {
-		root = definition.bones,
-		refs = {},
-		scale = definition.scale,
-		__noquickload = function()
-		end,
-		dirty = true,
-	}
-	local function dobone( b )
-		if b.name then
-			armature.refs[b.name] = b
-		end
-		b.transform = b.transform or Transform()
-		b.shape_offsets = {}
-		b.dirty = true
-		if b.shapes then
-			for name, transform in pairs( b.shapes ) do
-				table.insert( b.shape_offsets,
-				              { id = ids[name], tr = Transform( VecScale( transform.pos, definition.scale or 1 ), transform.rot ) } )
-			end
-		end
-		b.children = {}
-		for i = 1, #b do
-			b.children[i] = dobone( b[i] )
-		end
-		return b
-	end
-	dobone( armature.root )
-	return setmetatable( armature, armature_meta )
-end
-
----@type Armature
-
-local function computebone( bone, transform, scale, dirty )
-	dirty = dirty or bone.dirty or bone.jiggle_transform
-	if dirty or not bone.gr_transform then
-		bone.gr_transform = TransformToParentTransform( transform, bone.transform )
-		if bone.jiggle_transform then
-			bone.gr_transform = TransformToParentTransform( bone.gr_transform, bone.jiggle_transform )
-		end
-		bone.g_transform = Transform( VecScale( bone.gr_transform.pos, scale ), bone.gr_transform.rot )
-		bone.dirty = false
-	end
-	for i = 1, #bone.children do
-		computebone( bone.children[i], bone.gr_transform, scale, dirty )
-	end
-end
-
---- Computes the bone positions.
-function armature_meta:ComputeBones()
-	computebone( self.root, Transform(), self.scale or 1 )
-	self.dirty = false
-end
-
-local function applybone( shapes, bone )
-	for i = 1, #bone.shape_offsets do
-		local offset = bone.shape_offsets[i]
-		SetShapeLocalTransform( GetEntityHandle and GetEntityHandle( shapes[offset.id] ) or shapes[offset.id],
-		                        TransformToParentTransform( bone.g_transform, offset.tr ) )
-	end
-	for i = 1, #bone.children do
-		applybone( shapes, bone.children[i] )
-	end
-end
-
---- Applies the bone positions to a list of shapes.
----
----@param shapes Shape[] | number[]
-function armature_meta:Apply( shapes )
-	if self.dirty or self.jiggle then
-		self:ComputeBones()
-	end
-	applybone( shapes, self.root )
-end
-
---- Sets the local transform of a bone.
----
----@param bone string
----@param transform Transformation
-function armature_meta:SetBoneTransform( bone, transform )
-	local b = self.refs[bone]
-	if not b then
-		return
-	end
-	self.dirty = true
-	b.dirty = true
-	b.transform = transform
-end
-
---- Gets the local transform of a bone.
----
----@param bone string
----@return Transformation
-function armature_meta:GetBoneTransform( bone )
-	local b = self.refs[bone]
-	if not b then
-		return Transform()
-	end
-	return b.transform
-end
-
---- Gets the global transform of a bone.
----
----@param bone string
----@return Transformation
-function armature_meta:GetBoneGlobalTransform( bone )
-	local b = self.refs[bone]
-	if not b then
-		return Transform()
-	end
-	if self.dirty then
-		self:ComputeBones()
-	end
-	return b.g_transform
-end
-
----@alias JiggleConstaint { gravity?: number }
-
---- Sets the jiggle constraints of a bone.
----
----@param bone string
----@param jiggle number
----@param constraint? JiggleConstaint
-function armature_meta:SetBoneJiggle( bone, jiggle, constraint )
-	local b = self.refs[bone]
-	if not b then
-		return
-	end
-	self.dirty = true
-	if jiggle > 0 then
-		self.jiggle = true
-	end
-	b.jiggle = math.atan( jiggle ) / math.pi * 2
-	b.jiggle_constraint = constraint
-end
-
---- Gets the jiggle constraints of a bone.
----
----@param bone string
----@return number jiggle
----@return JiggleConstaint constraints
-function armature_meta:GetBoneJiggle( bone )
-	local b = self.refs[bone]
-	if not b then
-		return 0
-	end
-	return b.jiggle, b.jiggle_constraint
-end
-
---- Resets the jiggle state of all bones.
-function armature_meta:ResetJiggle()
-	for _, b in pairs( self.refs ) do
-		b.jiggle_transform = nil
-	end
-	self.dirty = true
-end
-
-local function updatebone( bone, current_transform, prev_transform, dt, gravity )
-	local current_transform_local = TransformToParentTransform( current_transform, bone.transform )
-	local prev_transform_local = TransformToParentTransform( prev_transform, bone.old_transform or bone.transform )
-	bone.old_transform = bone.transform
-	if bone.jiggle then
-		prev_transform_local = TransformToParentTransform( prev_transform_local, bone.jiggle_transform or Transform() )
-
-		local local_diff = TransformToLocalTransform( current_transform_local, prev_transform_local )
-		local target = TransformToParentPoint( local_diff, Vec( 0, 0, -2 / dt ) )
-
-		if bone.jiggle_constraint and bone.jiggle_constraint.gravity then
-			target = VecAdd( target,
-			                 TransformToLocalVec( current_transform_local, VecScale( gravity, bone.jiggle_constraint.gravity ) ) )
-		end
-
-		local lookat = QuatLookAt( Vec(), target )
-
-		bone.jiggle_transform = Transform( Vec(), QuatSlerp( lookat, QuatEuler( 0, 0, 0 ), 1 - bone.jiggle ) )
-		current_transform_local = TransformToParentTransform( current_transform_local, bone.jiggle_transform )
-	end
-	for i = 1, #bone.children do
-		updatebone( bone.children[i], current_transform_local, prev_transform_local, dt, gravity )
-	end
-end
-
---- Updates the physics of the armature.
----
----@param diff Transformation
----@param dt number
----@param gravity? Vector
-function armature_meta:UpdatePhysics( diff, dt, gravity )
-	dt = dt or 0.01666
-	diff.pos = VecScale( diff.pos, 1 / dt )
-	updatebone( self.root, Transform(), diff, dt, gravity or Vec( 0, -10, 0 ) )
-end
-
-local function DebugAxis( tr, s )
-	s = s or 1
-	DebugLine( tr.pos, TransformToParentPoint( tr, Vec( 1 * s, 0, 0 ) ), 1, 0, 0 )
-	DebugLine( tr.pos, TransformToParentPoint( tr, Vec( 0, 1 * s, 0 ) ), 0, 1, 0 )
-	DebugLine( tr.pos, TransformToParentPoint( tr, Vec( 0, 0, 1 * s ) ), 0, 0, 1 )
-end
-
---- Draws debug info of the armature at the specified transform.
----
----@param transform? Transformation
-function armature_meta:DrawDebug( transform )
-	transform = transform or Transform()
-	DebugAxis( transform, 0.05 )
-	for k, v in pairs( self.refs ) do
-		local r = TransformToParentTransform( transform, v.g_transform )
-		local g = v.name:find( "^__FIXED_" ) and 1 or 0
-		for i = 1, #v.children do
-			DebugLine( r.pos, TransformToParentTransform( transform, v.children[i].g_transform ).pos, 1, 1 - g, g, .4 )
-		end
-		for i = 1, #v.shape_offsets do
-			local offset = v.shape_offsets[i]
-			local p = TransformToParentTransform( transform, TransformToParentTransform( v.g_transform, offset.tr ) )
-			DebugAxis( p, 0.03 )
-			DebugLine( r.pos, p.pos, 0, 1, 1, .4 )
-		end
-	end
-end
-
- end)();
---src/tool/tool.lua
-(function() ----------------
--- Tool Framework
--- @script tool.tool
-
----@class Tool
----@field _TRANSFORM Transformation
----@field _TRANSFORM_FIX Transformation
----@field _TRANSFORM_DIFF Transformation
----@field _ARMATURE Armature
----@field _TOOLAMMOSTRING string
----@field armature Armature
----@field _SHAPES Shape[]
----@field _OBJECTS table[]
----@field model string
----@field printname string
----@field id string
-local tool_meta
-tool_meta = global_metatable( "tool", nil, true )
-
-local extra_tools = {}
-
---- Registers a tool using UMF.
----
----@param id string
----@param data table
----@return Tool
-function RegisterToolUMF( id, data )
-	if LoadArmatureFromXML and type( data.model ) == "table" then
-		local arm, xml = LoadArmatureFromXML( data.model.prefab, data.model.objects, data.model.scale )
-		data.armature = arm
-		data._ARMATURE = arm
-		data._OBJECTS = data.model.objects
-		local function findvox( xml )
-			if xml.type == "vox" then
-				return xml.attributes["file"]
-			end
-			for i, c in ipairs( xml.children ) do
-				local t = findvox( c )
-				if t then
-					return t
-				end
-			end
-		end
-		data.model = data.model.path or findvox( xml )
-	end
-	setmetatable( data, tool_meta )
-	data.id = id
-	extra_tools[id] = data
-	RegisterTool( id, data.printname or id, data.model or "", data.group or 6 )
-	SetBool( "game.tool." .. id .. ".enabled", true )
-	for k, f in pairs( tool_meta._C ) do
-		local v = rawget( data, k )
-		if v ~= nil then
-			rawset( data, k, nil )
-			f( data, v )
-		end
-	end
-	return data
-end
-
----@type Tool
-
-function tool_meta._C:ammo( val )
-	local key = "game.tool." .. self.id .. ".ammo"
-	local keystr = key .. ".display"
-	if val ~= nil then
-		if type( val ) == "number" then
-			SetFloat( key, val )
-			ClearKey( keystr )
-			rawset( self, "_TOOLAMMOSTRING", false )
-		else
-			SetFloat( key, 0 )
-			SetString( key .. ".display", tostring( val ) )
-			rawset( self, "_TOOLAMMOSTRING", tostring( val ) )
-		end
-	elseif HasKey( keystr ) then
-		return GetString( keystr )
-	else
-		return GetFloat( key )
-	end
-end
-
-function tool_meta._C:enabled( val )
-	local key = "game.tool." .. self.id .. ".enabled"
-	if val ~= nil then
-		SetBool( key, val )
-	else
-		return GetBool( key )
-	end
-end
-
---- Draws the tool in the world instead of the player view.
----
----@param transform Transformation
-function tool_meta:DrawInWorld( transform )
-	SetToolTransform( TransformToLocalTransform( GetCameraTransform(), transform ) )
-end
-
---- Gets the transform of the tool.
----
----@return Transformation
-function tool_meta:GetTransform()
-	return self._TRANSFORM or MakeTransformation( GetBodyTransform( GetToolBody() ) )
-end
-
---- Gets the predicted transform of the tool.
----
----@return Transformation
-function tool_meta:GetPredictedTransform()
-	return self._TRANSFORM_FIX or MakeTransformation( GetBodyTransform( GetToolBody() ) )
-end
-
---- Gets the transform delta of the tool.
----
----@return Transformation
-function tool_meta:GetTransformDelta()
-	return self._TRANSFORM_DIFF or Transformation( Vec(), Quat() )
-end
-
---- Gets the transform of a bone on the tool in world-space.
----
----@param bone string
----@param nopredicted? boolean
----@return Transformation
-function tool_meta:GetBoneGlobalTransform( bone, nopredicted )
-	if not self._ARMATURE then
-		return Transformation( Vec(), Quat() )
-	end
-	return (nopredicted and self:GetTransform() or self:GetPredictedTransform()):ToGlobal(
-		       self._ARMATURE:GetBoneGlobalTransform( bone ) )
-end
-
---- Draws the debug armature of the tool.
----
----@param nobones? boolean Don't draw bones.
----@param nobounds? boolean Don't draw bounds.
----@param nopredicted? boolean Don't use the predicted transform.
-function tool_meta:DrawDebug( nobones, nobounds, nopredicted )
-	if not self._ARMATURE or not self._SHAPES then
-		return
-	end
-	local ptr = (nopredicted and self:GetTransform() or self:GetPredictedTransform())
-	if not nobones and self._ARMATURE then
-		self._ARMATURE:DrawDebug( ptr )
-	end
-	if not nobounds and self._OBJECTS then
-		local s = self._OBJECTS
-		for i = 1, #self._SHAPES do
-			visual.drawbox( ptr:ToGlobal( self._SHAPES[i]:GetLocalTransform() ), Vec( 0, 0, 0 ),
-			                VecScale( s[#s + 1 - i][2], .05 ), { r = 1, g = 1, b = 1, a = .2, writeZ = false } )
-		end
-	end
-end
-
---- Callback called when the level loads.
-function tool_meta:Initialize()
-end
-
---- Callback called when tick() is called.
----
----@param dt number
-function tool_meta:Tick( dt )
-end
-
---- Callback called when draw() is called.
----
----@param dt number
-function tool_meta:Draw( dt )
-end
-
---- Callback called to animate the armature.
----
----@param body Body
----@param shapes Shape[]
-function tool_meta:Animate( body, shapes )
-end
-
---- Callback called when the tool is deployed.
-function tool_meta:Deploy()
-end
-
---- Callback called when the tool is holstered.
-function tool_meta:Holster()
-end
-
-local function istoolactive()
-	return GetBool( "game.player.canusetool" )
-end
-
-local prev
-hook.add( "api.mouse.wheel", "api.tool_loader", function( ds )
-	if not istoolactive() then
-		return
-	end
-	local tool = prev and extra_tools[prev]
-	if tool and tool.MouseWheel then
-		tool:MouseWheel( ds )
-	end
-end )
-
-hook.add( "base.update", "api.tool_loader", function( dt )
-	local cur = GetString( "game.player.tool" )
-	local tool = extra_tools[cur]
-	if tool then
-		if tool.Update then
-			softassert( pcall( tool.Update, tool, dt ) )
-		end
-	end
-end )
-
-hook.add( "base.tick", "api.tool_loader", function( dt )
-	local cur = GetString( "game.player.tool" )
-
-	local prevtool = prev and extra_tools[prev]
-	if prevtool then
-		if prevtool.ShouldLockMouseWheel then
-			local s, b = softassert( pcall( prevtool.ShouldLockMouseWheel, prevtool ) )
-			if s then
-				SetBool( "game.input.locktool", not not b )
-			end
-			if b then
-				SetString( "game.player.tool", prev )
-				cur = prev
-			end
-		end
-		if prev ~= cur and prevtool.Holster then
-			softassert( pcall( prevtool.Holster, prevtool ) )
-		end
-	end
-
-	local tool = extra_tools[cur]
-	if tool then
-		if prev ~= cur then
-			if tool.Deploy then
-				softassert( pcall( tool.Deploy, tool ) )
-			end
-			if tool._ARMATURE then
-				tool._ARMATURE:ResetJiggle()
-			end
-		end
-		local body = GetToolBody()
-		if not tool._BODY or tool._BODY.handle ~= body then
-			tool._BODY = Body( body )
-			tool._SHAPES = tool._BODY and tool._BODY:GetShapes()
-		end
-		if tool._BODY then
-			tool._TRANSFORM = tool._BODY:GetTransform()
-			tool._TRANSFORM_DIFF = tool._TRANSFORM_OLD and tool._TRANSFORM:ToLocal( tool._TRANSFORM_OLD ) or
-				                       Transformation( Vec(), Quat() )
-			local reverse_diff = tool._TRANSFORM_OLD and tool._TRANSFORM_OLD:ToLocal( tool._TRANSFORM ) or
-				                     Transformation( Vec(), Quat() )
-			-- reverse_diff.pos = VecScale(reverse_diff.pos, 60 * dt)
-			tool._TRANSFORM_FIX = tool._TRANSFORM:ToGlobal( reverse_diff )
-			if tool.Animate then
-				softassert( pcall( tool.Animate, tool, tool._BODY, tool._SHAPES ) )
-			end
-			if tool._ARMATURE then
-				tool._ARMATURE:UpdatePhysics( tool:GetTransformDelta(), GetTimeStep(),
-				                              TransformToLocalVec( tool:GetTransform(), Vec( 0, -10, 0 ) ) )
-				tool._ARMATURE:Apply( tool._SHAPES )
-			end
-		end
-		if tool._TOOLAMMOSTRING then
-			-- Fix sandbox ammo string
-			SetInt( "game.tool." .. tool.id .. ".ammo", 0 )
-		end
-		if tool.Tick then
-			softassert( pcall( tool.Tick, tool, dt ) )
-		end
-		if tool._TRANSFORM then
-			tool._TRANSFORM_OLD = tool._TRANSFORM
-		end
-	end
-	prev = cur
-end )
-
-hook.add( "api.firsttick", "api.tool_loader", function()
-	for id, tool in pairs( extra_tools ) do
-		if tool.Initialize then
-			softassert( pcall( tool.Initialize, tool ) )
-		end
-	end
-end )
-
-hook.add( "base.draw", "api.tool_loader", function( dt )
-	local tool = extra_tools[GetString( "game.player.tool" )]
-	if tool and tool.Draw then
-		softassert( pcall( tool.Draw, tool, dt ) )
-	end
-end )
-
-hook.add( "api.mouse.pressed", "api.tool_loader", function( button )
-	local tool = extra_tools[GetString( "game.player.tool" )]
-	local event = button == "lmb" and "LeftClick" or "RightClick"
-	if tool and tool[event] and istoolactive() then
-		softassert( pcall( tool[event], tool ) )
-	end
-end )
-
-hook.add( "api.mouse.released", "api.tool_loader", function( button )
-	local tool = extra_tools[GetString( "game.player.tool" )]
-	local event = button == "lmb" and "LeftClickReleased" or "RightClickReleased"
-	if tool and tool[event] and istoolactive() then
-		softassert( pcall( tool[event], tool ) )
-	end
-end )
-
- end)();
---src/tdui/base.lua
-(function() 
---[[
--- prototype code (desired outcome)
-TDUI.Label = TDUI.Panel {
-
-	text = ""
-	font = RegisterFont("font/consolas.ttf"),
-	fontSize = 24,
-
-	Draw = function(self, w, h)
-		UiFont(self.font, self.fontSize)
-		UiAlign("left top")
-		UiText(self.text)
-		-- This example doesn't account for:
-		--  * custom alignment
-		--  * wrapping on width
-		--  * Layout calculation
-	end,
-}
-
-local window = TDUI.Frame {
-	title = "Test Window",
-
-	width = "80%h",
-	height = "80%h",
-	resizeable = true,
-
-	padding = 10,
-
-	TDUI.Label {
-		text = "Something"
-	}
-}
-]]
-
-local function createchild( self, def )
-	setmetatable( def, { __index = self, __call = createchild, __PANEL = true } )
-	if self and self.__PerformInherit then
-		self:__PerformInherit( def )
-	end
-	if def.__PerformRegister then
-		def:__PerformRegister()
-	end
-	return def
-end
-
-TDUI = createchild( nil, {} )
-
-local function parseFour( data )
-	local dtype = type( data )
-	if dtype == "number" then
-		return { data, data, data, data }
-	elseif dtype == "string" then
-		local tmp = {}
-		for match in data:gmatch( "[^ ]+" ) do
-			tmp[#tmp + 1] = tonumber( match )
-		end
-		data = tmp
-		dtype = "table"
-	end
-	if dtype == "table" then
-		if #data == 0 then
-			return { 0, 0, 0, 0 }
-		end
-		if #data == 1 then
-			return { data[1], data[1], data[1], data[1] }
-		end
-		if #data < 4 then
-			return { data[1], data[2], data[1], data[2] }
-		end
-		return data
-	end
-	return { 0, 0, 0, 0 }
-end
-
-local function parsePos( data, w, h, def )
-	if type( data ) == "number" then
-		return data
-	end
-	if type( data ) == "function" then
-		return data( w, h, def )
-	end
-	if type( data ) ~= "string" then
-		return 0
-	end
-	if data:find( "function" ) then
-		return 0
-	end
-
-	local code = "local _,_w,_h = ...\nreturn" .. data:gsub( "(-?)([%d.]+)(%%?)([wh]?)", function( sub, n, prc, mod )
-		if prc == "" and mod == "" then
-			return sub .. n
-		end
-		return sub .. "(" .. n .. "*_" .. mod .. ")"
-	end )
-	local fn, err = loadstring( code )
-	assert( fn, err )
-	setfenv( fn, {} )
-
-	return fn( def / 100, w / 100, h / 100 )
-end
-
-local function parseAlign( data )
-	local alignx, aligny = 1, 1
-	for str in data:gmatch( "%w+" ) do
-		if str == "left" then
-			alignx = 1
-		end
-		if str == "center" then
-			alignx = 0
-		end
-		if str == "right" then
-			alignx = -1
-		end
-		if str == "top" then
-			aligny = 1
-		end
-		if str == "middle" then
-			aligny = 0
-		end
-		if str == "bottom" then
-			aligny = -1
-		end
-	end
-	return alignx, aligny
-end
-
-TDUI.Slot = function( name )
-	return { __SLOT = name }
-end
-
--- Base Panel,
-TDUI.Panel = TDUI {
-	__alignx = 1,
-	__aligny = 1,
-	__realx = 0,
-	__realy = 0,
-	__realw = 0,
-	__realh = 0,
-	margin = { 0, 0, 0, 0 },
-	padding = { 0, 0, 0, 0 },
-	boxsizing = "parent",
-	align = "left top",
-	clip = false,
-	visible = true,
-
-	layout = TDUI.Layout,
-
-	oninit = function( self )
-	end,
-
-	predraw = function( self, w, h )
-	end,
-	ondraw = function( self, w, h )
-		-- UiColor(1, 1, 1)
-		-- UiTranslate(-40, -40)
-		-- UiImageBox("common/box-solid-shadow-50.png", w+80, h+81, 50, 50)
-		-- UiTranslate(40, 40)
-		-- UiColor(1, 0, 0, 0.2)
-		-- UiRect(w, h)
-	end,
-	postdraw = function( self, w, h )
-	end,
-
-	__Draw = function( self )
-		if not self.visible then
-			return
-		end
-		if not rawget( self, "__validated" ) then
-			self:InvalidateLayout( true )
-		end
-		local w, h = self:GetComputedSize()
-		self:predraw( w, h )
-		self:ondraw( w, h )
-
-		if self.clip then
-			UiPush()
-			UiWindow( w, h, true )
-		end
-
-		local x, y = 0, 0
-		for i = 1, #self do
-			local child = self[i]
-			local dfx, dfy = child:GetComputedPos()
-			UiTranslate( dfx - x, dfy - y )
-			child:__Draw()
-			x, y = dfx, dfy
-		end
-		UiTranslate( -x, -y )
-
-		if self.clip then
-			UiPop()
-		end
-
-		self:postdraw( w, h )
-	end,
-
-	__PerformRegister = function( self )
-		self.margin = parseFour( self.margin )
-		self.padding = parseFour( self.padding )
-		self.__alignx, self.__aligny = parseAlign( self.align )
-		local i = 1
-		self.__dynamic = {}
-		local hasslots, slots = false, rawget( self, "__SLOTS" ) or {}
-		while i <= #self do
-			if type( self[i] ) == "function" or (type( self[i] ) == "table" and type( self[i].__SLOT ) == "string") then
-				local id = #self.__dynamic + 1
-				local result
-				if self[i] == TDUI.Slot or (type( self[i] ) == "table" and type( self[i].__SLOT ) == "string") then
-					local name = self[i] == TDUI.Slot and "default" or self[i].__SLOT
-					result = {}
-					local content
-					slots[name] = function( c )
-						content = c
-						self:__RefreshDynamic( id )
-					end
-					self.__dynamic[id] = {
-						func = function()
-							return content
-						end,
-						min = i,
-						count = 0,
-					}
-					hasslots = true
-				else
-					result = self[i]( self, id )
-					self.__dynamic[id] = { func = self[i], min = i, count = #result }
-				end
-				if #result == 0 then
-					table.remove( self, i )
-				elseif #result == 1 then
-					self[i] = result[1]
-				else
-					for j = #self, i + 1, -1 do
-						self[j + #result - 1] = self[j]
-					end
-					for j = 1, #result do
-						self[i + j - 1] = result[j]
-					end
-				end
-				i = i - 1
-			else
-				local cslots = rawget( self[i], "__SLOTS" )
-				if cslots then -- TODO: WHY DOES THIS SECTION WORK???
-					hasslots = true -- need to use __dynamic to make sure the right child is being referenced
-					for name, update in pairs( cslots ) do
-						slots[name] = update
-					end
-					self[i].__SLOTS = nil
-				end
-				rawset( self[i], "__parent", self )
-			end
-			i = i + 1
-		end
-		if hasslots then
-			self.__SLOTS = slots
-		end
-		self:oninit()
-	end,
-
-	__PerformInherit = function( self, child )
-		local SLOTS = rawget( self, "__SLOTS" )
-		if SLOTS then
-			for name, update in pairs( SLOTS ) do
-				local src = name == "default" and child or child[name]
-				update( src )
-			end
-		end
-		if SLOTS and SLOTS.default then
-			for i = 1, #child do
-				child[i] = nil
-			end
-		end
-		if #self > 0 then
-			for i = #child, 1, -1 do
-				child[i + #self] = child[i]
-			end
-			for i = 1, #self do
-				local meta = getmetatable( self[i] )
-				if meta and meta.__PANEL then
-					child[i] = self[i] {}
-				else
-					child[i] = self[i]
-				end
-			end
-		end
-	end,
-
-	__RefreshDynamic = function( self, id )
-		local dyn = self.__dynamic[id]
-		if not dyn then
-			return
-		end
-		local result = dyn.func( self, id )
-		local d = #result - dyn.count
-		if d > 0 then
-			for i = #self, dyn.min + dyn.count, -1 do
-				self[i + d] = self[i]
-			end
-		elseif d < 0 then
-			for i = dyn.min + dyn.count, #self - d do
-				self[i + d] = self[i]
-			end
-		end
-		for i = 1, #result do
-			self[dyn.min + i - 1] = result[i]
-		end
-		dyn.count = #result
-		for i = id + 1, #self.__dynamic do
-			self.__dynamic[i].min = self.__dynamic[i].min + d
-		end
-		self:InvalidateLayout()
-	end,
-
-	onlayout = function( self, data, pw, ph, ew, eh )
-		-- onlayout must do 2 things:
-		--  1. Position its children within the available space
-		--  2. Compute its own size for the layout of its parent
-
-		-- TODO: Optimize for static sizes and unchanged bounds
-
-		local selflayout = self.layout
-		if selflayout then
-			local f = selflayout.onlayout
-			if f and f ~= self.onlayout then
-				return f( self, selflayout, pw, ph, ew, eh )
-			end
-		end
-		warning( "Unable to compute layout" )
-		self.__validated = true
-		self:ComputeSize( pw, ph )
-		for i = 1, #self do
-			local child = self[i]
-			child:onlayout( child, self.__realw, self.__realh, self.__realw, self.__realh )
-			child:ComputePosition( 0, 0, self.__realw, self.__realh )
-		end
-		return self.__realw, self.__realh
-
-		--[[self.__realx = self.x and parsePos(self.x, pw, ph, pw) or 0
-		self.__realy = self.y and parsePos(self.y, pw, ph, ph) or 0
-		self.__realw = self.width and parsePos(self.width, pw, ph, pw) or 256
-		self.__realh = self.height and parsePos(self.height, pw, ph, ph) or 256
-		self.__validated = true
-		for i = 1, #self do
-			local child = self[i]
-			child:__PerformLayout(self.__realw, self.__realh)
-		end]]
-	end,
-
-	ComputePosition = function( self, dx, dy, pw, ph )
-		if self.boxsizing == "parent" then
-			local parent = self:GetParent()
-			if parent then
-				pw = pw - self.margin[4] - self.margin[2]
-				ph = ph - self.margin[1] - self.margin[3]
-			end
-		end
-
-		local x = self.x and parsePos( self.x, pw, ph, pw ) or 0
-		if self.__alignx == 1 then
-			self.__realx = x + self.margin[4] + dx
-		elseif self.__alignx == 0 then
-			self.__realx = x + (pw - self.__realw) / 2 + dx
-		elseif self.__alignx == -1 then
-			self.__realx = x + pw - self.margin[2] - self.__realw + dx
-		end
-
-		local y = self.y and parsePos( self.y, pw, ph, ph ) or 0
-		if self.__aligny == 1 then
-			self.__realy = y + self.margin[1] + dy
-		elseif self.__aligny == 0 then
-			self.__realy = y + (ph - self.__realh) / 2 + dy
-		elseif self.__aligny == -1 then
-			self.__realy = y + ph - self.margin[3] - self.__realh + dy
-		end
-
-		return self.__realx, self.__realy
-	end,
-
-	ComputeSize = function( self, pw, ph )
-		if self.boxsizing == "parent" then
-			local parent = self:GetParent()
-			if parent then
-				pw = pw - self.margin[4] - self.margin[2]
-				ph = ph - self.margin[1] - self.margin[3]
-			end
-		end
-		self.__realw = (self.width and parsePos( self.width, pw, ph, pw ) or 0)
-		self.__realh = (self.height and parsePos( self.height, pw, ph, ph ) or 0)
-		if self.ratio then
-			if self.width and not self.height then
-				self.__realh = self.__realw * self.ratio
-			elseif self.height and not self.width then
-				self.__realw = self.__realh / self.ratio
-			end
-		end
-		return self.__realw - self.padding[4] - self.padding[2], self.__realh - self.padding[1] - self.padding[3]
-	end,
-
-	InvalidateLayout = function( self, immediate )
-		if immediate then
-			local cw, ch = self:GetComputedSize()
-			local pw, ph = self:GetParentSize()
-			self:onlayout( self, pw, ph, self.__prevew or pw, self.__preveh or ph )
-			local nw, nh = self:GetComputedSize()
-			if nw ~= cw or nh ~= ch then
-				self:InvalidateParentLayout( true )
-			end
-		else
-			self.__validated = false
-		end
-	end,
-
-	InvalidateParentLayout = function( self, immediate )
-		local parent = self:GetParent()
-		if parent then
-			return parent:InvalidateLayout( immediate )
-		else
-			local pw, ph = UiWidth(), UiHeight()
-			self:InvalidateLayout( immediate )
-			self.__realx = self.x and parsePos( self.x, pw, ph, pw ) or 0
-			self.__realy = self.y and parsePos( self.y, pw, ph, ph ) or 0
-		end
-	end,
-
-	SetParent = function( self, parent )
-		local prev = self:GetParent()
-		if prev then
-			for i = 1, #prev do
-				if prev[i] == self then
-					table.remove( prev, i )
-					prev:InvalidateLayout()
-					break
-				end
-			end
-		end
-		if parent then
-			parent[#parent + 1] = self
-			rawset( self, "__parent", parent )
-			parent:InvalidateLayout()
-		end
-	end,
-
-	GetParent = function( self )
-		return rawget( self, "__parent" )
-	end,
-
-	GetComputedPos = function( self )
-		return self.__realx, self.__realy
-	end,
-
-	GetComputedSize = function( self )
-		return self.__realw, self.__realh
-	end,
-
-	SetSize = function( self, w, h )
-		self.width, self.height = w, h
-		self:InvalidateLayout()
-	end,
-	SetWidth = function( self, w )
-		self.width = w
-		self:InvalidateLayout()
-	end,
-	SetHeight = function( self, h )
-		self.height = h
-		self:InvalidateLayout()
-	end,
-
-	SetPos = function( self, x, y )
-		self.x, self.y = x, y
-		self:InvalidateLayout()
-	end,
-	SetX = function( self, x )
-		self.x = x
-		self:InvalidateLayout()
-	end,
-	SetY = function( self, y )
-		self.y = y
-		self:InvalidateLayout()
-	end,
-
-	SetMargin = function( self, top, right, bottom, left )
-		if right then
-			top = { top, right, bottom, left }
-		end
-		self.margin = parseFour( top )
-		self:InvalidateLayout()
-	end,
-
-	SetPadding = function( self, top, right, bottom, left )
-		if right then
-			top = { top, right, bottom, left }
-		end
-		self.padding = parseFour( top )
-		self:InvalidateLayout()
-	end,
-
-	GetParentSize = function( self )
-		local parent = self:GetParent()
-		if parent then
-			return parent:GetComputedSize()
-		else
-			return UiWidth(), UiHeight()
-		end
-	end,
-
-	Hide = function( self )
-		self.visible = false
-	end,
-	Show = function( self )
-		self.visible = true
-	end,
-}
-
-TDUI.Layout = TDUI.Panel {
-	onlayout = function( self, data, pw, ph, ew, eh )
-		self.__validated = true
-		self.__prevew, self.__preveh = ew, eh
-		local nw, nh = self:ComputeSize( pw, ph )
-		local p1, p2, p3, p4 = self.padding[1], self.padding[2], self.padding[3], self.padding[4]
-		for i = 1, #self do
-			local child = self[i]
-			child:onlayout( child, nw, nh, ew, eh )
-			child:ComputePosition( p4, p1, nw, nh )
-		end
-		return self.__realw + self.margin[4] + self.margin[2], self.__realh + self.margin[1] + self.margin[3]
-	end,
-}
-
-TDUI.SimpleForEach = function( tab, callback )
-	return function()
-		local rt = {}
-		for i = 1, #tab do
-			local e = callback( tab[i], i, tab )
-			if e then
-				rt[#rt + 1] = e
-			end
-		end
-		return rt
-	end
-end
-
-TDUI.Panel.layout = TDUI.Layout
-
-local ScreenPanel = TDUI.Panel { x = 0, y = 0, width = 0, height = 0 }
-
-function TDUI.Panel:Popup( parent )
-	self:SetParent( parent or ScreenPanel )
-end
-
-function TDUI.Panel:Close()
-	self:SetParent()
-end
-
-hook.add( "base.draw", "api.tdui.ScreenPanel", function()
-	if ScreenPanel.width == 0 then
-		ScreenPanel:SetSize( UiWidth(), UiHeight() )
-	end
-	UiPush()
-	softassert( pcall( ScreenPanel.__Draw, ScreenPanel ) )
-	UiPop()
-end )
-
- end)();
---src/tdui/image.lua
-(function() 
-TDUI.Image = TDUI.Panel {
-	path = "",
-	fit = "fit",
-
-	ondraw = function( self, w, h )
-		if not HasFile( self.path ) then
-			return
-		end
-		local iw, ih = self:GetImageSize()
-		UiPush()
-		if self.fit == "stretch" then
-			UiScale( w / iw, h / ih )
-		elseif self.fit == "cover" then
-			local r, ir = w / h, iw / ih
-			UiWindow( w, h, true )
-			if r > ir then
-				UiTranslate( 0, h / 2 - ih * w / iw / 2 )
-				UiScale( w / iw )
-			else
-				UiTranslate( w / 2 - iw * h / ih / 2, 0 )
-				UiScale( h / ih )
-			end
-		elseif self.fit == "fit" then
-			local r, ir = w / h, iw / ih
-			if r > ir then
-				UiTranslate( w / 2 - iw * h / ih / 2, 0 )
-				UiScale( h / ih )
-			else
-				UiTranslate( 0, h / 2 - ih * w / iw / 2 )
-				UiScale( w / iw )
-			end
-		end
-		self:DrawImage( iw, ih )
-		UiPop()
-	end,
-
-	GetImageSize = function( self )
-		return UiGetImageSize( self.path )
-	end,
-	DrawImage = function( self, w, h )
-		UiImage( self.path )
-	end,
-}
-
-TDUI.AtlasImage = TDUI.Image {
-	atlas_width = 1,
-	atlas_height = 1,
-	atlas_x = 1,
-	atlas_y = 1,
-
-	GetImageSize = function( self )
-		local iw, ih = UiGetImageSize( self.path )
-		return iw / self.atlas_width, ih / self.atlas_height
-	end,
-	DrawImage = function( self, w, h )
-		UiWindow( w, h, true )
-		UiTranslate( (1 - self.atlas_x) * w, (1 - self.atlas_y) * h )
-		UiImage( self.path )
-	end,
-}
-
- end)();
---src/tdui/layout.lua
-(function() 
-TDUI.StackLayout = TDUI.Layout {
-	orientation = "vertical",
-
-	onlayout = function( self, data, pw, ph, ew, eh )
-		self.__validated = true
-		self.__prevew, self.__preveh = ew, eh
-		local isvertical = data.orientation == "vertical"
-		local nw, nh = self:ComputeSize( pw, ph )
-		local pdw, pdh = self.padding[4] + self.padding[2], self.padding[1] + self.padding[3]
-		local nfw, nfh = nw == -pdw, nh == -pdh
-		if not nfw then
-			ew = nw
-		else
-			ew = ew - pdw
-		end
-		if not nfh then
-			eh = nh
-		else
-			eh = eh - pdh
-		end
-		if isvertical then
-			if nfh then
-				nh = 0
-			end
-		else
-			if nfw then
-				nw = 0
-			end
-		end
-		for i = 1, #self do
-			local child = self[i]
-			local cw, ch = child:onlayout( child, nw, nh, ew, eh )
-			if isvertical then
-				if nfw and cw > nw and cw <= ew then
-					nw = cw
-				end
-				if nfh then
-					nh = nh + ch
-				end
-			else
-				if nfw then
-					nw = nw + cw
-				end
-				if nfh and ch > nh and ch <= eh then
-					nh = ch
-				end
-			end
-		end
-		local dx, dy = self.padding[4], self.padding[1]
-		for i = 1, #self do
-			local child = self[i]
-			local cw, ch = child:onlayout( child, nw, nh, ew, eh )
-			child:ComputePosition( dx, dy, nw, nh )
-			if isvertical then
-				dy = dy + ch
-			else
-				dx = dx + cw
-			end
-		end
-		if nfw then
-			self.__realw = nw + pdw
-		end
-		if nfh then
-			self.__realh = nh + pdh
-		end
-		return self.__realw + self.margin[4] + self.margin[2], self.__realh + self.margin[1] + self.margin[3]
-	end,
-}
-
-TDUI.WrapLayout = TDUI.Layout {
-	orientation = "vertical",
-
-	onlayout = function( self, data, pw, ph, ew, eh )
-		self.__validated = true
-		self.__prevew, self.__preveh = ew, eh
-		local isvertical = data.orientation == "vertical"
-		local nw, nh = self:ComputeSize( pw, ph )
-		local pdw, pdh = self.padding[4] + self.padding[2], self.padding[1] + self.padding[3]
-		local nfw, nfh = nw == -pdw, nh == -pdh
-		if not nfw then
-			ew = nw
-		else
-			ew = ew - pdw
-		end
-		if not nfh then
-			eh = nh
-		else
-			eh = eh - pdh
-		end
-		if isvertical then
-			if nfh then
-				nh = 0
-			end
-		else
-			if nfw then
-				nw = 0
-			end
-		end
-		for i = 1, #self do
-			local child = self[i]
-			local cw, ch = child:onlayout( child, nw, nh, ew, eh )
-			if isvertical then
-				if nfw and cw > nw and cw <= ew then
-					nw = cw
-				end
-				if nfh then
-					nh = nh + ch
-				end
-			else
-				if nfw then
-					nw = nw + cw
-				end
-				if nfh and ch > nh and ch <= eh then
-					nh = ch
-				end
-			end
-		end
-		local dx, dy = self.padding[4], self.padding[1]
-		local curr = 0
-		for i = 1, #self do
-			local child = self[i]
-			local cw, ch = child:onlayout( child, nw, nh, ew, eh )
-			if isvertical then
-				if nw + pdw < dx + cw then
-					dx = self.padding[4]
-					dy = dy + curr
-					curr = 0
-				end
-				child:ComputePosition( dx, dy, nw, nh )
-				curr = math.max( curr, ch )
-				dx = dx + cw
-			else
-				if nh + pdh < dy + ch then
-					dy = self.padding[1]
-					dx = dx + curr
-					curr = 0
-				end
-				child:ComputePosition( dx, dy, nw, nh )
-				curr = math.max( curr, cw )
-				dy = dy + ch
-			end
-		end
-		if nfw then
-			self.__realw = nw + pdw
-		end
-		if nfh then
-			self.__realh = nh + pdh
-		end
-		return self.__realw + self.margin[4] + self.margin[2], self.__realh + self.margin[1] + self.margin[3]
-	end,
-}
-
- end)();
---src/tdui/panel.lua
-(function() 
-TDUI.SlicePanel = TDUI.Panel {
-	color = { 1, 1, 1, 1 },
-
-	predraw = function( self, w, h )
-		UiPush()
-		UiColor( self.color[1] or 1, self.color[2] or 1, self.color[3] or 1, self.color[4] or 1 )
-		local t = self.template
-		UiTranslate( -t.offset_left, -t.offset_top )
-		UiImageBox( t.image, w + t.offset_left + t.offset_right, h + t.offset_top + t.offset_bottom, t.slice_x, t.slice_y )
-		UiPop()
-	end,
-}
-
-TDUI.SlicePanel.SolidShadow50 = {
-	image = "ui/common/box-solid-shadow-50.png",
-	slice_x = 50,
-	slice_y = 50,
-	offset_left = 40,
-	offset_top = 40,
-	offset_bottom = 41,
-	offset_right = 40,
-}
-
-TDUI.SlicePanel.template = TDUI.SlicePanel.SolidShadow50
-
- end)();
---src/tdui/window.lua
-(function() 
-TDUI.Window = TDUI.Panel {
-	color = { 1, 1, 1, 1 },
-
-	predraw = function( self, w, h )
-	end,
-
-	TDUI.Panel { TDUI.Slot "title" },
-
-	TDUI.Panel { TDUI.Slot },
-}
-
- end)();
---src/_index.lua
-(function() -- 
- end)();
-for i = 1, #__RUNLATER do local f = loadstring(__RUNLATER[i]) if f then pcall(f) end end

```

---

# Migration Report: TDSU\util_camera.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/TDSU\util_camera.lua
+++ patched/TDSU\util_camera.lua
@@ -1,6 +1,4 @@
-Cameras = {}
-
-
+#version 2
 function Camera_create(x, y, zoom)
 
 	local camera = {
@@ -36,28 +34,3 @@
 
 end
 
-
--- function GetCrosshairWorldPos(pos, rejectBodies)
-
---     local crosshairTr = GetCrosshairWorldPos()
---     RejectAllBodies(rejectBodies)
---     local crosshairHit, crosshairHitPos = RaycastFromTransform(crosshairTr, 500)
---     if crosshairHit then
---         return crosshairHitPos
---     else
---         return nil
---     end
-
--- end
-
--- function GetCrosshairCameraTr(pos, x, y)
-
---     pos = pos or GetCameraTransform()
-
---     local crosshairDir = UiPixelToWorld(x or UiCenter(), y or UiMiddle())
---     local crosshairQuat = DirToQuat(crosshairDir)
---     local crosshairTr = Transform(GetCameraTransform().pos, crosshairQuat)
-
---     return crosshairTr
-
--- end
```

---

# Migration Report: TDSU\util_cmd.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/TDSU\util_cmd.lua
+++ patched/TDSU\util_cmd.lua
@@ -1,3 +1,4 @@
+#version 2
 function handleCommand(cmd)
     HandleQuickload(cmd)
 end
@@ -13,3 +14,4 @@
         break
     end
 end
+

```

---

# Migration Report: TDSU\util_color.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/TDSU\util_color.lua
+++ patched/TDSU\util_color.lua
@@ -1,6 +1,4 @@
---[[DEBUG COLOR]]
-
-
+#version 2
 function InitColor()
 
     Colors = {
@@ -44,8 +42,5 @@
 
 end
 
+function Color(color) return table.unpack(color) end
 
-
----Return r,g,b values of a Color sub-table.
----@param color table Color from Colors table.
-function Color(color) return table.unpack(color) end
```

---

# Migration Report: TDSU\util_debug.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/TDSU\util_debug.lua
+++ patched/TDSU\util_debug.lua
@@ -1,18 +1,9 @@
-db_groups = {
-    override = false, -- Force all db functions on.
-    mod = true,
-}
-
-
+#version 2
 function InitDebug()
     DB = GetBool('savegame.mod.debugModeMaster')
     db = GetBool('savegame.mod.debugMode')
 end
 
-
----Handles the toggling of debug mode.
----@param DB boolean Debug debugger.
----@param db boolean Debug mod.
 function TickDebug(DB, db)
 
     DB = GetBool('savegame.mod.debugModeMaster')
@@ -27,56 +18,53 @@
 
 end
 
-
 function ToggleDb()
-    SetBool('savegame.mod.debugMode', not GetBool('savegame.mod.debugMode'))
+    SetBool('savegame.mod.debugMode', not GetBool('savegame.mod.debugMode'), true)
     db = GetBool('savegame.mod.debugMode')
     print("db mode: " .. Ternary(db, 'on\t', 'off\t') .. sfnTime())
     -- ternary(db, beepOn, beepOff)()
 end
 
 function ToggleDB()
-    SetBool('savegame.mod.debugModeMaster', not GetBool('savegame.mod.debugModeMaster'))
+    SetBool('savegame.mod.debugModeMaster', not GetBool('savegame.mod.debugModeMaster'), true)
     DB = GetBool('savegame.mod.debugModeMaster')
     print("DB mode: " .. Ternary(DB, 'on\t', 'off\t') .. sfnTime())
     -- ternary(DB, beepOn, beepOff)()
 end
 
-
----Run a function if db is true.
----@param func function The global function to run.
----@param tb_args table Table of arguements for the function.
 function dbfunc(func, tb_args) if db then func(table.unpack(tb_args)) end end
 
+function dbw(str, value) if db then DebugWatch(str, value) end end
 
---[[DEBUG CONSOLE]]
-function dbw(str, value) if db then DebugWatch(str, value) end end -- DebugWatch()
-function dbp(str) if db then print(str .. '(' .. sfnTime() .. ')') end end -- DebugPrint()
-function dbpc(str, newLine) if db then print(str .. Ternary(newLine, '\n', '')) end end -- DebugPrint() to external console window only.
-function dbpt(tb) if db then PrintTable(tb) end end -- PrintTable() to external console window.
+function dbp(str) if db then print(str .. '(' .. sfnTime() .. ')') end end
 
+function dbpc(str, newLine) if db then print(str .. Ternary(newLine, '\n', '')) end end
 
---[[DEBUG 3D]]
-function dbl(p1, p2, r,g,b,a, dt) if db then DebugLine(p1, p2, r,g,b,a, dt) end end -- DebugLine()
-function dbdd(pos, w,l, r,g,b,a, dt) if db then DrawDot(pos,w,l,r,g,b,a,dt) end end -- Draw a dot sprite at the specified position.
-function dbray(tr, dist, r,g,b,a) dbl(tr.pos, TransformToParentPoint(tr, Vec(0,0,-dist)), c1, c2, c3, a) end -- Debug a ray segement from a transform.
-function dbcr(pos, r,g,b, a) if db then DebugCross(pos, r or 1, g or 1, b or 1, a or 1) end end -- DebugCross() at a specified position.
+function dbpt(tb) if db then PrintTable(tb) end end
+
+function dbl(p1, p2, r,g,b,a, dt) if db then DebugLine(p1, p2, r,g,b,a, dt) end end
+
+function dbdd(pos, w,l, r,g,b,a, dt) if db then DrawDot(pos,w,l,r,g,b,a,dt) end end
+
+function dbray(tr, dist, r,g,b,a) dbl(tr.pos, TransformToParentPoint(tr, Vec(0,0,-dist)), c1, c2, c3, a) end
+
+function dbcr(pos, r,g,b, a) if db then DebugCross(pos, r or 1, g or 1, b or 1, a or 1) end end
 
 function dbpath(tb_points, tb_color, a, dots) --- Draw the lines between an ipair table of points. Gradient between tables tb_rgba1 and tb_rgba2.
     DebugPath(tb_points, tb_color, a, dots)
 end
 
+function DebugRay(tr, dist, r,g,b,a) DebugLine(tr.pos, TransformToParentPoint(tr, Vec(0,0,-dist)), r or 1, g or 1, b or 1, a or 1) end
 
-function DebugRay(tr, dist, r,g,b,a) DebugLine(tr.pos, TransformToParentPoint(tr, Vec(0,0,-dist)), r or 1, g or 1, b or 1, a or 1) end -- Debug a ray segement from a transform.
+function beep(pos, vol) PlaySound(LoadSound("warning-beep"),    pos or GetCameraTransform().pos, vol or 0.5) end
 
+function buzz(pos, vol) PlaySound(LoadSound("light/spark0"),    pos or GetCameraTransform().pos, vol or 0.5) end
 
+function chime(pos, vol) PlaySound(LoadSound("elevator-chime"), pos or GetCameraTransform().pos, vol or 0.5) end
 
-
---[[DEBUG SOUNDS]]
-function beep(pos, vol) PlaySound(LoadSound("warning-beep"),    pos or GetCameraTransform().pos, vol or 0.5) end
-function buzz(pos, vol) PlaySound(LoadSound("light/spark0"),    pos or GetCameraTransform().pos, vol or 0.5) end
-function chime(pos, vol) PlaySound(LoadSound("elevator-chime"), pos or GetCameraTransform().pos, vol or 0.5) end
 function shine(pos, vol) PlaySound(LoadSound("valuable.ogg"),   pos or GetCameraTransform().pos, vol or 0.5) end
 
 function beepOn(pos, vol) PlaySound(LoadSound("MOD/TDSU/snd/beep-on.ogg"),   pos or GetCameraTransform().pos, vol or 0.3) end
+
 function beepOff(pos, vol) PlaySound(LoadSound("MOD/TDSU/snd/beep-off.ogg"),   pos or GetCameraTransform().pos, vol or 0.3) end
+

```

---

# Migration Report: TDSU\util_env.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/TDSU\util_env.lua
+++ patched/TDSU\util_env.lua
@@ -1,15 +1,4 @@
-env_types = {
-    string = "string",
-    float = "float",
-    int = "int",
-    euler = "euler",
-    vec_euler = "vec_euler",
-    vec_rad = "vec_rad",
-    vec_dir = "dir",
-}
-
-
-
+#version 2
 function env_type_string()
     return {
         type = "string",
@@ -69,8 +58,6 @@
     }
 
 end
-
-
 
 function Get_EnvironmentSettings()
 
@@ -173,7 +160,6 @@
 
 end
 
-
 function InitEnv()
 
     -- PrintTable(GetCurrentEnv())
@@ -185,7 +171,6 @@
     }
 
 end
-
 
 function Draw_EnvSettingsMenu()
 
@@ -217,7 +202,6 @@
         AutoSpreadEnd()
     UiPop() end
 
-
     ScrollY = ScrollY or 0
     ScrollY = clamp(ScrollY - (InputValue("mousewheel") * 32), 0, math.huge)
 
@@ -263,7 +247,6 @@
             UiTranslate(-30/2/2, ScrollY)
             AutoImage("ui/common/dot.png", 20, 30)
 
-
         AutoSpreadEnd()
 
     UiPop()
@@ -273,222 +256,6 @@
 function ProcessEnvs()
 end
 
-
-MenuItems = {
-    Skybox = {
-        skybox = {
-            type = "",
-            name = "Skybox",
-            desc = "The dds file used as skybox.\nSearch path is data/env.",
-            string = true,
-            dd = {
-                "cannon_2k.dds", "cloudy.dds", "cold_dramatic_clouds.dds",
-                "cold_sunny_evening.dds", "cold_sunset.dds",
-                "cold_wispy_sky.dds", "cool_clear_sunrise.dds", "cool_day.dds",
-                "day.dds", "industrial_sunset_2k.dds", "jk2.dds", "moonlit.dds",
-                "night.dds", "night_clear.dds", "overcast_day.dds",
-                "sunflowers_2k.dds", "sunset.dds",
-                "sunset_in_the_chalk_quarry_2k.dds", "tornado.dds"
-            }
-        },
-        skyboxtint = {
-            type = "",
-            name = "Skybox Tint",
-            desc = "The skybox color tint",
-            args = 3,
-            color = true
-        },
-        skyboxbrightness = {
-            type = "",
-            name = "Skybox Brightness",
-            desc = "The skybox brightness scale"
-        },
-        skyboxrot = {
-            type = "",
-            name = "Skybox Rotation",
-            desc = "The skybox rotation around the y axis.\nUse this to determine angle of sun shadows."
-        }
-    },
-    Sun = {
-        sunBrightness = {
-            type = "",
-            name = "Sun Brightness",
-            desc = "Light contribution by sun (gives directional shadows)"
-        },
-        sunColorTint = {
-            type = "",
-            name = "Sun Tint",
-            desc = "Color tint of sunlight.\nMultiplied with brightest spot in skybox",
-            args = 3,
-            color = true
-        },
-        sunDir = {
-            type = "",
-            name = "Sun Direction",
-            desc = "Direction of sunlight. A value of zero\nwill point from brightest spot in skybox",
-            args = 3
-        },
-        sunSpread = {
-            type = "",
-            name = "Sun Spread",
-            desc = "Divergence of sunlight as a fraction. A value\nof 0.05 will blur shadows 5 cm per meter"
-        },
-        sunLength = {
-            type = "",
-            name = "Sun Length",
-            desc = "Maximum length of sunlight shadows.\nAS low as possible for best performance"
-        },
-        sunFogScale = {
-            type = "",
-            name = "Sun Fog Scale",
-            desc = "Volumetic fog caused by sunlight"
-        },
-        sunGlare = {
-            type = "",
-            name = "Sun Glare",
-            desc = "Sun glare scaling"}
-    },
-    Fog = {
-        fogColor = {
-            type = "",
-            name = "Fog Color",
-            desc = "Color used for distance fog",
-            args = 3,
-            color = true
-        },
-        fogParams = {
-            type = "",
-            name = "Fog Parameters",
-            desc = "Four fog parameters: fog start, fog end, fog amount,\nfog exponent (higher gives steeper falloff along y axis)",
-            args = 4
-        },
-        fogscale = {
-            type = "",
-            name = "Fog Scale",
-            desc = "Scale fog value on all light sources with this amount"
-        }
-    },
-    Lighting = {
-        constant = {
-            type = "",
-            name = "Constant Light",
-            desc = "Base light, always contributes no matter\nlighting conditions.",
-            args = 3
-        },
-        ambient = {
-            type = "",
-            name = "Ambient Light",
-            desc = "Determines how much the skybox will\nlight up the scene."
-        },
-        ambientexponent = {
-            type = "",
-            name = "Ambient Exponent",
-            desc = "Determines ambient light falloff when occluded.\nHigher value = darker indoors."
-        },
-        exposure = {
-            type = "",
-            name = "Exposure Limits",
-            desc = "Limits for automatic exposure, min max",
-            args = 2
-        },
-        brightness = {
-            type = "",
-            name = "Brightness",
-            desc = "Desired scene brightness that controls\nautomatic exposure. Set higher for brighter scene."
-        },
-        nightlight = {
-            type = "",
-            name = "Night Lights",
-            desc = "If set to false, all lights tagged night will be removed.",
-            bool = true
-        }
-    },
-    Rain = {
-        wetness = {
-            type = "",
-            name = "Wetness",
-            desc = "Base wetness"},
-        puddleamount = {
-            type = "",
-            name = "Puddle Amount",
-            desc = "Puddle coverage. Fraction between zero and one"
-        },
-        puddlesize = {
-            type = "",
-            name = "Puddle Size",
-            desc = "Puddle size"},
-        rain = {
-            type = "",
-            name = "Rain Amount",
-            desc = "Amount of rain"}
-    },
-    Snow = {
-        snowdir = {
-            type = "",
-            name = "Snow Direction",
-            desc = "Snow direction, x, y, z, and spread"
-        },
-        snowamount = {
-            type = "",
-            name = "Snow Amount",
-            desc = "Snow particle amount (0-1)"},
-        snowonground = {
-            type = "",
-            name = "Snow on Ground",
-            desc = "Generate snow on ground",
-            bool = true
-        }
-    },
-    Misc = {
-        ambience = {
-            type = "",
-            name = "Ambience",
-            desc = "Environment sound path",
-            string = true,
-            dd = {
-                "indoor/cave.ogg", "indoor/dansband.ogg", "indoor/factory.ogg",
-                "indoor/factory0.ogg", "indoor/factory1.ogg",
-                "indoor/factory2.ogg", "indoor/mall.ogg",
-                "indoor/small_room0.ogg", "indoor/small_room1.ogg",
-                "indoor/small_room2.ogg", "indoor/small_room3.ogg",
-                "outdoor/caribbean.ogg", "outdoor/caribbean_ocean.ogg",
-                "outdoor/field.ogg", "outdoor/forest.ogg", "outdoor/lake.ogg",
-                "outdoor/lake_birds.ogg", "outdoor/night.ogg",
-                "outdoor/ocean.ogg", "outdoor/rain_heavy.ogg",
-                "outdoor/rain_light.ogg", "outdoor/wind.ogg",
-                "outdoor/winter.ogg", "outdoor/winter_snowstorm.ogg",
-                "woonderland/lee_woonderland_cabins.ogg",
-                "woonderland/lee_woonderland_freefall.ogg",
-                "woonderland/lee_woonderland_motorcycles.ogg",
-                "woonderland/lee_woonderland_sea_side_swings.ogg",
-                "woonderland/lee_woonderland_swanboats.ogg",
-                "woonderland/lee_woonderland_tire_carousel.ogg",
-                "woonderland/lee_woonderland_wheel_of_woo.ogg",
-                "woonderland/lee_woonderland_woocars.ogg", "underwater.ogg"
-            }
-        },
-        slippery = {
-            type = "",
-            name = "Slipperiness",
-            desc = "Slippery road. Affects vehicles when outdoors"
-        },
-        waterhurt = {
-            type = "",
-            name = "Water Damage",
-            desc = "Players take damage being in water. If above zero,\nhealth will decrease and not regenerate in water"
-        },
-        wind = {
-            type = "",
-            name = "Wind Strength",
-            desc = "Wind direction and strength: x y z",
-            args = 3
-        } -- I dunno, don't ask?
-    }
-}
-
-
-
--- Get current environment properties and format it as a lua table, printed to the console.
 function GetCurrentEnv()
 
     local env = {}
@@ -529,4 +296,5 @@
 
     return env
 
-end+end
+

```

---

# Migration Report: TDSU\util_lua.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/TDSU\util_lua.lua
+++ patched/TDSU\util_lua.lua
@@ -1,158 +1,4 @@
---[[TABLES]]
-do
-
-    ---Clone a table without any links to the original.
-    function DeepCopy(tb_orig)
-        local orig_type = type(tb_orig)
-        local copy
-        if orig_type == 'table' then
-            copy = {}
-            for orig_key, orig_value in next, tb_orig, nil do
-                copy[DeepCopy(orig_key)] = DeepCopy(orig_value)
-            end
-            setmetatable(copy, DeepCopy(getmetatable(tb_orig)))
-        else -- number, string, boolean, etc
-            copy = tb_orig
-        end
-        return copy
-    end
-
-    ---Get a random index of a table (not the value).
-    function GetRandomIndex(tb)
-        local i = math.random(1, #tb)
-        return i
-    end
-
-    ---Get a random index of a table (not the value).
-    function  GetRandomIndexValue(tb)
-        local i = math.random(1, #tb)
-        return tb[i]
-    end
-
-    ---Get the next index of a table (not the value). Loop to first index if on the last index.
-    function GetTableNextIndex(tb, i)
-        if i + 1 > #tb then
-            return 1
-        else
-            return i + 1
-        end
-    end
-
-    ---Get the previous index of a table (not the value). Loop to first index if on the last index.
-    function GetTablePreviousIndex(tb, i)
-        if i - 1 <= 0 then
-            return #tb
-        else
-            return i - 1
-        end
-    end
-
-    ---Swap 2 values in a table.
-    function TableSwapValue(tb, i1, i2)
-        local temp = DeepCopy(tb[i1])
-        tb[i1] = tb[i2]
-        tb[i2] = temp
-        return tb
-    end
-
-    function TableLength(tb)
-        local s = 0
-        for _ in pairs(tb) do s = s + 1 end
-        return s
-    end
-
-
-end
-
-
---[[FORMATTING]]
-do
-    ---(String Format Number) return a rounded number as a string.
-    function sfn(numberToFormat, dec) return string.format("%.".. (tostring(dec or 2)) .."f", numberToFormat) end
-
-    ---(String Format Time) Returns the time rounded to decimal as a string.
-    function sfnTime(dec) return sfn(' '..GetTime(), dec or 4) end
-
-    ---(String Format Commas) Returns a number formatted with commas as a string.
-    function sfnCommas(dec)
-        return tostring(math.floor(dec)):reverse():gsub("(%d%d%d)","%1,"):gsub(",(%-?)$","%1"):reverse()
-        -- https://stackoverflow.com/questions/10989788/format-integer-in-lua
-    end
-
-    ---(String Format Int) Returns a number formatted as an integer.
-    function sfnInt(n)
-        local s = tostring(n)
-        local int = ''
-        for i = 1, string.len(s) do
-            local c = string.sub(s, i, i)
-            if c == '.' then
-                return int
-            else
-                int = int .. c
-            end
-        end
-    end
-
-    function sfnPadZeroes(n, pad) return string.format('%0' .. tostring(pad or 2) .. 'd', n) end
-
-    function Ternary ( cond , T , F ) if cond then return T else return F end end
-
-    -- Conditionally run function.
-    function CondFunc(condition, func, tb_args)
-        if condition then
-            func(unpack(tb_args))
-        end
-    end
-
-    ---A helper function to print a table's contents.
-    ---@param tbl table @The table to print.
-    ---@param depth number @The depth of sub-tables to traverse through and print.
-    ---@param n number @Do NOT manually set this. This controls formatting through recursion.
-    function PrintTable(tbl, depth, n)
-        n = n or 0;
-        depth = depth or 10;
-
-        if (depth == 0) then
-            print(string.rep(' ', n).."...");
-            return;
-        end
-
-        if (n == 0) then
-            print(" ");
-        end
-
-        for key, value in pairs(tbl) do
-            if (key and type(key) == "number" or type(key) == "string") then
-                key = string.format("%s", key);
-
-                if (type(value) == "table") then
-                    if (next(value)) then
-                        print(string.rep(' ', n)..key.." = {");
-                        PrintTable(value, depth - 1, n + 4);
-                        print(string.rep(' ', n).."},");
-                    else
-                        print(string.rep(' ', n)..key.." = {},");
-                    end
-                else
-                    if (type(value) == "string") then
-                        value = string.format("\"%s\"", value);
-                    else
-                        value = tostring(value);
-                    end
-
-                    print(string.rep(' ', n)..key.." = "..value..",");
-                end
-            end
-        end
-
-        if (n == 0) then
-            print(" ");
-        end
-    end
-
-end
-
-
+#version 2
 function string_append(str, str_append, separator)
     return str .. Ternary(str == "" or str == nil, "", (separator or ", ")) .. str_append
 end
@@ -160,7 +6,6 @@
 function string_enclose(s, str_left, str_right)
     return str_left .. s .. (str_right or str_left)
 end
-
 
 function IsStringInteger(data)
     for i = 1, #data do
@@ -175,6 +20,3 @@
     return true
 end
 
-
--- function CallOnce()
--- end
```

---

# Migration Report: TDSU\util_math.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/TDSU\util_math.lua
+++ patched/TDSU\util_math.lua
@@ -1,124 +1,21 @@
---[[MATH]]
-do
-
-    -- If n is less than zero, return a small number.
-    function GTZero(n) if n <= 0 then return 1/math.huge end return n end
-
-    -- Return a positive non-zero number if n == 0.
-    function NZero(n) if n == 0 then return 1/math.huge end return n end
-
-    ---Return a random number.
-    function Random(min, max) return math.random(min, max - 1) + math.random() end
-
-    ---Contrain a number between two numbers.
-    function Clamp(value, min, max)
-        if value < min then value = min end
-        if value > max then value = max end
-        return value
-    end
-
-    ---Oscillate a value between 0 and 1 based on time.
-    ---@param time number Seconds to complete a oscillation period.
-    function Oscillate(time)
-        local a = ((-1/2) * math.cos(2 * math.pi * GetTime()/(time or 1))) + 0.5
-        return a
-    end
-
-    ---Linear interpolation between two values.
-    function Lerp(a,b,t) return a + (b-a) * 0.5 * t end
-
-    ---Round a number to n decimals.
-    function Round(x, n)
-        n = 10 ^ (n or 0)
-        x = x * n
-        if x >= 0 then x = math.floor(x + 0.5) else x = math.ceil(x - 0.5) end
-        return x / n
-    end
-
-    ---Approach a value at a specified rate.
-    function ApproachValue(value, target, rate)
-        if value >= target then
-
-            if value - rate < target then
-                return target
-            else
-                return value - rate
-            end
-
-        elseif value < target then
-
-            if value + rate > target then
-                return target
-            else
-                return value + rate
-            end
-
-        end
-    end
-
-end
-
+#version 2
 function avg(a, b)
     return (a+b)/2
 end
+
 function slope(x1, y1, x2, y2)
     return (y2-y1)/(x2-x1)
 end
+
 function hyp(x, y) --- Return hypotenuse.
     return math.sqrt(x^2 + y^2)
 end
 
----Returns a convex parabola starting at x=0, ending at x=1 and its center vertex at y=1.
----@param n number A number between 0 and 1.
----@return number
 function getQuadtratic(n)
     return -4 * ( n -0.5) ^ 2 + 1
 end
 
---[[QUERY]]
-do
-    ---Raycast from a transform.
-    ---@param tr table -- Source transform.
-    ---@param dist number -- Max raycast distance. Default is 300.
-    ---@param rad number -- Raycast radius/thickness.
-    ---@param rejectBodies table -- Table of bodies to query reject.
-    ---@param rejectShapes table -- Table of shapes to query reject.
-    ---@param returnNil bool -- If true, return nil if no raycast hit. If false, return the end point of the raycast based on the transfom and distance.
-    ---@return h boolean hit
-    ---@return p table hit position
-    ---@return d number hit dist
-    ---@return s number hit shape
-    ---@return b number hit body
-    ---@return n table normal
-    function RaycastFromTransform(tr, dist, rad, rejectBodies, rejectShapes, returnNil)
-
-        dist = dist or 300
-
-        if rejectBodies ~= nil then for i = 1, #rejectBodies do QueryRejectBody(rejectBodies[i]) end end
-        if rejectShapes ~= nil then for i = 1, #rejectShapes do QueryRejectShape(rejectShapes[i]) end end
-
-        local direction = QuatToDir(tr.rot)
-        local h, d, n, s = QueryRaycast(tr.pos, direction, dist, rad)
-        if h then
-
-            local p = TransformToParentPoint(tr, Vec(0, 0, d * -1))
-            local b = GetShapeBody(s)
-            return h, p, d, s, b, n
-
-        elseif not returnNil then
-            return false, TransformToParentPoint(tr, Vec(0,0,-dist))
-        else
-            return nil
-        end
-
-    end
-
-end
-
-
---[[BOOLEAN]]
 function boolflip(bool) return not bool end
-
 
 function clamp(val, lower, upper)
     if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
@@ -136,3 +33,4 @@
 function CompressRange(val, lower, upper)
     return (val-lower) / (upper-lower)
 end
+

```

---

# Migration Report: TDSU\util_quat.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/TDSU\util_quat.lua
+++ patched/TDSU\util_quat.lua
@@ -1,36 +1 @@
---[[QUAT]]
-do
-
-    -- Quat to normalized dir.
-    function QuatToDir(quat)
-        return TransformToParentVec(Transform(Vec(), quat), Vec(0,0,-1))
-    end
-
-    -- Normalized dir to quat.
-    function DirToQuat(dir) return QuatLookAt(Vec(0,0,0), dir) end
-
-    -- Normalized dir of two positions.
-    function DirLookAt(eye, target) return VecNormalize(VecSub(target, eye)) end
-
-    -- Angle between two vectors.
-    function VecAngle(a,b) return math.deg(math.acos(VecDot({a[1], a[2], a[3]}, {b[1], b[2], b[3]}) / (VecLength(c) * VecLength(d)))) end
-
-    -- Angle between two vectors.
-    function QuatAngle(a,b)
-        av = QuatToDir(a)
-        bv = QuatToDir(b)
-        local c = {av[1], av[2], av[3]}
-        local d = {bv[1], bv[2], bv[3]}
-        return math.deg(math.acos(VecDot(c, d) / (VecLength(c) * VecLength(d))))
-    end
-
-    function QuatLookUp() return DirToQuat(Vec(0, 1, 0)) end -- Quat facing world-up.
-    function QuatLookDown() return DirToQuat(Vec(0, -1, 0)) end -- Quat facing world-down.
-
-    function QuatTrLookUp(tr) return QuatLookAt(tr.pos, TransformToParentPoint(tr, Vec(0,1,0))) end -- Quat look above tr.
-    function QuatTrLookDown(tr) return QuatLookAt(tr.pos, TransformToParentPoint(tr, Vec(0,-1,0))) end -- Quat look below tr.
-    function QuatTrLookLeft(tr) return QuatLookAt(tr.pos, TransformToParentPoint(tr, Vec(-1,0,0))) end -- Quat look left of tr.
-    function QuatTrLookRight(tr) return QuatLookAt(tr.pos, TransformToParentPoint(tr, Vec(1,0,0))) end -- Quat look right of tr.
-    function QuatTrLookBack(tr) return QuatLookAt(tr.pos, TransformToParentPoint(tr, Vec(0,0,1))) end -- Quat look behind tr.
-
-end
+#version 2

```

---

# Migration Report: TDSU\util_td.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/TDSU\util_td.lua
+++ patched/TDSU\util_td.lua
@@ -1,6 +1,7 @@
+#version 2
 function AimSteerVehicle()
 
-    local v = GetPlayerVehicle()
+    local v = GetPlayerVehicle(playerId)
     if v ~= 0 then AimSteerVehicle(v) end
 
     local vTr = GetVehicleTransform(v)
@@ -13,76 +14,7 @@
 
 end
 
+function RejectAllBodies(bodies) for i = 1, #bodies do QueryRejectBody(bodies[i]) end end
 
-function RejectAllBodies(bodies) for i = 1, #bodies do QueryRejectBody(bodies[i]) end end
 function RejectAllShapes(shapes) for i = 1, #shapes do QueryRejectShape(shapes[i]) end end
 
-
--- function CheckExplosions(cmd)
-
---     words = splitString(cmd, " ")
---     if #words == 5 then
---         if words[1] == "explosion" then
-
---             local strength = tonumber(words[2])
---             local x = tonumber(words[3])
---             local y = tonumber(words[4])
---             local z = tonumber(words[5])
-
---             -- DebugPrint('explosion: ')
---             -- DebugPrint('strength: ' .. strength)
---             -- DebugPrint('x: ' .. x)
---             -- DebugPrint('y: ' .. y)
---             -- DebugPrint('z: ' .. z)
---             -- DebugPrint('')
-
---         end
---     end
-
---     if #words == 8 then
---         if words[1] == "shot" then
-
---             local strength = tonumber(words[2])
---             local x = tonumber(words[3])
---             local y = tonumber(words[4])
---             local z = tonumber(words[5])
---             local dx = tonumber(words[6])
---             local dy = tonumber(words[7])
---             local dz = tonumber(words[8])
-
---             -- DebugPrint('shot: ')
---             -- DebugPrint('strength: ' .. strength)
---             -- DebugPrint('x: ' .. x)
---             -- DebugPrint('y: ' .. y)
---             -- DebugPrint('z: ' .. z)
---             -- DebugPrint('dx: ' .. dx)
---             -- DebugPrint('dy: ' .. dy)
---             -- DebugPrint('dz: ' .. dz)
---             -- DebugPrint('')
-
---         end
---     end
-
--- end
-
-
--- function SetShapeCollision()
-    -- LAYER_A = 1 -- Default
-    -- LAYER_B = 2
-    -- LAYER_C = 4
-    -- LAYER_D = 8
-    -- LAYER_E = 16
-    -- LAYER_F = 32
-    -- LAYER_G = 64
-    -- LAYER_H = 128
-    -- EVERY_LAYER = 255
-
-    -- -- shape in layer D, collide only with layer B and C
-    -- SetShapeCollisionFilter(shape1, LAYER_D, LAYER_B + LAYER_C)
-    -- -- shape in layer E, do not collide with layer B and C
-    -- SetShapeCollisionFilter(shape2, LAYER_E, EVERY_LAYER - LAYER_B - LAYER_C)
-
-    -- -- Example
-    -- SetShapeCollisionFilter(engine, LAYER_B, EVERY_LAYER - LAYER_B)
-    -- SetShapeCollisionFilter(propeller, LAYER_B, EVERY_LAYER - LAYER_B)
--- end

```

---

# Migration Report: TDSU\util_timer.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/TDSU\util_timer.lua
+++ patched/TDSU\util_timer.lua
@@ -1,9 +1,4 @@
--- function TimerCreateSeconds(seconds, time)
---     time = time or 0
---     local timer = { time = 60/time, rpm = 60/seconds }
---     return timer
--- end
-
+#version 2
 function TimerCreateRPM(time, rpm)
 
     local timer = { time = time or 0, rpm = rpm }
@@ -12,10 +7,6 @@
 
 end
 
----Run a timer and a table of functions.
----@param timer table -- = {time, rpm}
----@param funcs_and_args table -- Table of functions that are called when time = 0. functions = {{func = func, args = {args}}}
----@param runTime boolean -- Decrement time when calling this function.
 function TimerRunTimer(timer, funcs_and_args, runTime)
     if timer.time <= 0 then
         TimerResetTime(timer)
@@ -29,17 +20,14 @@
     end
 end
 
--- Only runs the timer countdown if there is time left.
 function TimerRunTime(timer)
     timer.time = timer.time - GetTimeStep()
 end
 
--- Set time left to 0.
 function TimerEndTime(timer)
     timer.time = 0
 end
 
--- Reset time to start (60/rpm).
 function TimerResetTime(timer)
     timer.time = 60/timer.rpm
 end
@@ -48,7 +36,7 @@
     return timer.time <= 0
 end
 
--- Get the timer's completion fraction between 0 and 1.0. Timer consumed = 1.
 function TimerGetPhase(timer)
     return clamp(((60/timer.rpm) - timer.time) / (60/timer.rpm), 0, 1)
 end
+

```

---

# Migration Report: TDSU\util_tool.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/TDSU\util_tool.lua
+++ patched/TDSU\util_tool.lua
@@ -1,12 +1,8 @@
-TOOL = {} -- Game global tool.
-Tool = {} -- Actual tool.
-
-
+#version 2
 local id    = 'glowingSea'
 local name  = 'Glowing Sea'
 local file  = 'MOD/TDSU/tool/tool.vox'
 local group = 6
-
 
 function InitTool(Tool)
 
@@ -32,50 +28,46 @@
     Tool.isEnabled  = Tool_setEnabled
 
     RegisterTool(Tool.setup.id, Tool.setup.name, Tool.setup.file, Tool.setup.group)
-    SetBool('game.tool.'..Tool.setup.id..'.enabled', enabled or true)
+    SetBool('game.tool.'..Tool.setup.id..'.enabled', enabled or true, true)
 
 end
-
 
 function Tool_isActive(self, ignoreSafeMode)
 
     local isWeilding    = GetString('game.player.tool') == self.setup.id
-    local inVehicle     = ignoreSafeMode or (GetPlayerVehicle() ~= 0)
+    local inVehicle     = ignoreSafeMode or (GetPlayerVehicle(playerId) ~= 0)
     local isGrabbing    = ignoreSafeMode or GetString('game.player.grabbing') == self.setup.id
 
     return inVehicle and isWeilding and isGrabbing
 
 end
 
-
----Called in tick().
 function Tool_startWith(self)
     if TOOLSTART == nil then
-        SetString('game.player.tool', self.setup.id)
+        SetString('game.player.tool', self.setup.id, true)
         TOOLSTART = true -- Calls once only
     end
 end
+
 function Tool_switchTo(self)
-    SetString('game.player.tool', self.setup.id)
-end
-function Tool_lockScroll(self)
-    SetString('game.player.tool', self.setup.id)
+    SetString('game.player.tool', self.setup.id, true)
 end
 
+function Tool_lockScroll(self)
+    SetString('game.player.tool', self.setup.id, true)
+end
 
 function Tool_setEnabled(self, isEnabled)
-    SetBool('game.tool.'..self.setup.id..'.enabled', isEnabled)
+    SetBool('game.tool.'..self.setup.id..'.enabled', isEnabled, true)
 end
 
-
----Disable all tools except specified ones.
----@param allowTools table -- Table of strings (tool names) to ignore.
 function DisableTools(allowTools)
     -- local toolNames = {sledge = 'sledge', spraycan = 'spraycan', extinguisher ='extinguisher', blowtorch = 'blowtorch'}
     local tools = ListKeys("game.tool")
     for i = 1, #tools do
         -- if tools[i] ~= toolNames[tools[i]] then
-            SetBool("game.tool."..tools[i]..".enabled", false)
+            SetBool("game.tool."..tools[i]..".enabled", false, true)
         -- end
     end
 end
+

```

---

# Migration Report: TDSU\util_ui.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/TDSU\util_ui.lua
+++ patched/TDSU\util_ui.lua
@@ -1,3 +1,4 @@
+#version 2
 function margin(x,y) UiTranslate(x,y) end
 
 function uiDrawSquare()
@@ -32,12 +33,10 @@
     UiColor(1,1,1, 1)
 end
 
--- Draw the outline and highlight of a shape
 function uiDrawShape(s)
     DrawShapeOutline(s, 1,1,1, 1)
     DrawShapeHighlight(s, 0.25)
 end
-
 
 function createSlider(tb, key, title, valueText, min, max, w, h, fs)
 
@@ -177,4 +176,5 @@
 	else
 		UiColor(1,0,0, 1)
 	end
-end+end
+

```

---

# Migration Report: TDSU\util_umf.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/TDSU\util_umf.lua
+++ patched/TDSU\util_umf.lua
@@ -1,12 +1,4 @@
---================================================================
--- Functions for Thomasims' UMF Unofficial Modding Framework)
---================================================================
-
-
-
----Convert a umf shared table to a regular lua table. Mainly used to interate over the table. If there are no string keys the converted table will have numerical indicies.
----@param _path string Path to the table in the regsitry.
----@return table tb Converted table.
+#version 2
 function ConvertSharedTable(_path)
 
     local tb = {}
@@ -20,11 +12,6 @@
 
 end
 
-
----Build a single value from a umf shared table. Called recursively in ConvertSharedTable().
----@param tb table Table with values to build. Can be a nested table inside of an already built value.
----@param key string Key of the table in the registry (can be an index or key)
----@param _path string Path to the specified shared table index in the registry.
 function BuildSharedTableValue(tb, key, _path)
 
     local pathConc = conc(_path, {key})
@@ -68,3 +55,4 @@
     end
 
 end
+

```

---

# Migration Report: TDSU\util_vec.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/TDSU\util_vec.lua
+++ patched/TDSU\util_vec.lua
@@ -1,309 +1,8 @@
---[[VECTORS]]
-do
-    --- Distance between two vectors.
-    VecDist = function(v1, v2) return VecLength(VecSub(v1, v2)) end
-
-    --- Divide a vector by another vector's components.
-    VecDiv = function(v1, v2) return Vec(v1[1] / v2[1], v1[2] / v2[2], v1[3] / v2[3]) end
-
-    VecMult = function(v1, v2)
-        local v = Vec(0,0,0)
-        for i = 1, 3 do v[i] = v1[i] * v2[i] end
-        return v
-    end
-
-    --- Add a table of vectors together.
-    VecAddAll = function(tb_vecs) local v = Vec(0,0,0) for i = 1, #tb_vecs do VecAdd(v, tb_vecs[i]) end return v end
-
-    --- Returns a vector with random values.
-    VecRandom = function(length)
-        local v = VecNormalize(Vec(math.random(-10000000,10000000), math.random(-10000000,10000000), math.random(-10000000,10000000)))
-        return VecScale(v, length)
-    end
-
-    -- Return each min component.
-    function VecMin(v1, v2)
-        local v = Vec(0,0,0)
-        for i = 1, 3 do
-            v[i] = math.min(v1[i], v2[i])
-        end
-        return v
-    end
-
-    -- Return each max component.
-    function VecMax(v1, v2)
-        local v = Vec(0,0,0)
-        for i = 1, 3 do
-            v[i] = math.max(v1[i], v2[i])
-        end
-        return v
-    end
-
-    --- Print QuatEulers or vectors.
-    VecPrint = function(vec, label, decimals)
-
-        local str = (label or "")
-
-        str = string_append(str, sfn(vec[1], decimals))
-        str = string_append(str, sfn(vec[2], decimals), ", ")
-        str = string_append(str, sfn(vec[3], decimals), ", ")
-
-        str = string_enclose(str, "{", " }")
-
-        DebugPrint(str)
-        print(str)
-
-    end
-
-
-    --- Returns a vector with random values.
-    function VecRdm(length)
-        local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
-        return VecScale(v, length)
-    end
-
-    ---Move a point towards another point for a specified distance.
-    VecApproach = function(vec_start, vec_end, dist)
-        local sub_pos = VecScale(VecNormalize(VecSub(vec_end, vec_start)), dist)
-        return VecAdd(vec_start, sub_pos)
-    end
-
-    ---Average vector between two vectors.
-    VecAvg = function(v1, v2) return VecScale(VecAdd(v1, v2), 1/2) end
-
-    ---Return the x value of a Vec.
-    vx = function(v) return v[1] or v.x end
-
-    ---Return the y value of a Vec.
-    vy = function(v) return v[2] or v.y end
-
-    ---Return the z value of a Vec.
-    vz = function(v) return v[3] or v.z end
-
-    ---Takes a table a like { x = 0, y = 0, z = 0 } and converts it to Vec(0,0,0)
-    ToVec = function(v) return Vec(v.x, v.y, v.z) end
-
-    ---Takes a Vec like and Vec(0,0,0) converts it to { x = 0, y = 0, z = 0 }
-    ToCompVec = function(v) return { x = v[1], y = v[2], z = v[3] } end
-
-    TransformAdd = function(tr1, tr2)
-        return Transform(VecAdd(tr1.pos, tr2.pos), QuatRotateQuat(tr1.rot, tr2.rot))
-    end
-
-    TransformAdd = function(tr1, tr2)
-        return Transform(VecAdd(tr1.pos, tr2.pos), QuatRotateQuat(tr1.rot, tr2.rot))
-    end
-
-end
-
-
---[[AABB]]
-do
-    AabbDimensions = function(min, max) return Vec(max[1] - min[1], max[2] - min[2], max[3] - min[3]) end
-    AabbDraw = function(v1, v2, r, g, b, a)
-        r = r or 1 g = g or 1 b = b or 1 a = a or 1
-        local x1 = v1[1] local y1 = v1[2] local z1 = v1[3] local x2 = v2[1] local y2 = v2[2] local z2 = v2[3]
-        -- x lines top
-        DebugLine(Vec(x1,y1,z1), Vec(x2,y1,z1), r, g, b, a)
-        DebugLine(Vec(x1,y1,z2), Vec(x2,y1,z2), r, g, b, a)
-        -- x lines bottom
-        DebugLine(Vec(x1,y2,z1), Vec(x2,y2,z1), r, g, b, a)
-        DebugLine(Vec(x1,y2,z2), Vec(x2,y2,z2), r, g, b, a)
-        -- y lines
-        DebugLine(Vec(x1,y1,z1), Vec(x1,y2,z1), r, g, b, a)
-        DebugLine(Vec(x2,y1,z1), Vec(x2,y2,z1), r, g, b, a)
-        DebugLine(Vec(x1,y1,z2), Vec(x1,y2,z2), r, g, b, a)
-        DebugLine(Vec(x2,y1,z2), Vec(x2,y2,z2), r, g, b, a)
-        -- z lines top
-        DebugLine(Vec(x2,y1,z1), Vec(x2,y1,z2), r, g, b, a)
-        DebugLine(Vec(x2,y2,z1), Vec(x2,y2,z2), r, g, b, a)
-        -- z lines bottom
-        DebugLine(Vec(x1,y1,z2), Vec(x1,y1,z1), r, g, b, a)
-        DebugLine(Vec(x1,y2,z2), Vec(x1,y2,z1), r, g, b, a)
-    end
-    AabbCheckOverlap = function(aMin, aMax, bMin, bMax)
-        return
-        (aMin[1] <= bMax[1] and aMax[1] >= bMin[1]) and
-        (aMin[2] <= bMax[2] and aMax[2] >= bMin[2]) and
-        (aMin[3] <= bMax[3] and aMax[3] >= bMin[3])
-    end
-    AabbCheckPointInside = function(aMin, aMax, pos)
-        return
-        (pos[1] <= aMax[1] and pos[1] >= aMin[1]) and
-        (pos[2] <= aMax[2] and pos[2] >= aMin[2]) and
-        (pos[3] <= aMax[3] and pos[3] >= aMin[3])
-    end
-    AabbClosestEdge = function(pos, shape)
-        local shapeAabbMin, shapeAabbMax = GetShapeBounds(shape)
-        local bCenterY = VecLerp(shapeAabbMin, shapeAabbMax, 0.5)[2]
-        local edges = {}
-        edges[1] = Vec(shapeAabbMin[1], bCenterY, shapeAabbMin[3]) -- a
-        edges[2] = Vec(shapeAabbMax[1], bCenterY, shapeAabbMin[3]) -- b
-        edges[3] = Vec(shapeAabbMin[1], bCenterY, shapeAabbMax[3]) -- c
-        edges[4] = Vec(shapeAabbMax[1], bCenterY, shapeAabbMax[3]) -- d
-
-        local closestEdge = edges[1] -- find closest edge
-        local index = 1
-        for i = 1, #edges do
-            local edge = edges[i]
-
-            local edgeDist = VecDist(pos, edge)
-            local closesEdgeDist = VecDist(pos, closestEdge)
-
-            if edgeDist < closesEdgeDist then
-                closestEdge = edge
-                index = i
-            end
-        end
-        return closestEdge, index
-    end
-    --- Sort edges by closest to startPos and closest to endPos. Return sorted table.
-    AabbSortEdges = function(startPos, endPos, edges)
-        local s, startIndex = aabbClosestEdge(startPos, edges)
-        local e, endIndex = aabbClosestEdge(endPos, edges)
-        --- Swap first index with startPos and last index with endPos. Everything between stays same.
-        edges = tableSwapIndex(edges, 1, startIndex)
-        edges = tableSwapIndex(edges, #edges, endIndex)
-        return edges
-    end
-
-
-
-    -- Shape center
-    function AabbGetShapeCenterPos(shape)
-        local mi, ma = GetShapeBounds(shape)
-        return VecLerp(mi,ma,0.5)
-    end
-    -- Shape center top
-    function AabbGetShapeCenterTopPos(shape, addY)
-        addY = addY or 0
-        local mi, ma = GetShapeBounds(shape)
-        local v =  VecLerp(mi,ma,0.5)
-        v[2] = ma[2] + addY
-        return v
-    end
-    -- Shape center bottom
-    function AabbGetShapeCenterBottomPos(shape, addY)
-        addY = addY or 0
-        local mi, ma = GetShapeBounds(shape)
-        local v =  VecLerp(mi,ma,0.5)
-        v[2] = mi[2] + addY
-        return v
-    end
-
-
-
-    -- Body center
-    function AabbGetBodyCenterPos(body)
-        local mi, ma = GetBodyBounds(body)
-        return VecLerp(mi,ma,0.5)
-    end
-    -- Body center top
-    function AabbGetBodyCenterTopPos(body, addY)
-        addY = addY or 0
-        local mi, ma = GetBodyBounds(body)
-        local v =  VecLerp(mi,ma,0.5)
-        v[2] = ma[2] + addY
-        return v
-    end
-    -- Body center top
-    function AabbGetBodyCenterBottomPos(body, addY)
-        addY = addY or 0
-        local mi, ma = GetBodyBounds(body)
-        local v =  VecLerp(mi,ma,0.5)
-        v[2] = mi[2] + addY
-        return v
-    end
-
-end
-
---[[OBB]]
-do
-    ObbDrawShape = function(shape)
-
-        local shapeTr = GetShapeWorldTransform(shape)
-        local shapeDim = VecScale(Vec(sx, sy, sz), 0.1)
-        local maxTr = Transform(TransformToParentPoint(shapeTr, shapeDim), shapeTr.rot)
-
-        for i = 1, 3 do
-
-            local vec = Vec(0,0,0)
-
-            vec[i] = shapeDim[i]
-
-            DebugLine(shapeTr.pos, maxTr.pos)
-            DebugLine(shapeTr.pos, TransformToParentPoint(shapeTr, vec), 0,1,0, 1)
-            DebugLine(maxTr.pos, TransformToParentPoint(maxTr, VecScale(vec, -1)), 1,0,0, 1)
-
-        end
-
-    end
-end
-
---[[PHYSICS]]
-do
-    -- Reduce the angular body velocity by a certain rate each frame.
-    DiminishBodyAngVel = function(body, rate)
-        local av = GetBodyAngularVelocity(body)
-        local dRate = rate or 0.99
-        local diminishedAngVel = Vec(av[1]*dRate, av[2]*dRate, av[3]*dRate)
-        SetBodyAngularVelocity(body, diminishedAngVel)
-    end
-    IsMaterialUnbreakable = function(mat, shape)
-        return mat == 'rock' or mat == 'heavymetal' or mat == 'unbreakable' or mat == 'hardmasonry' or
-            HasTag(shape,'unbreakable') or HasTag(GetShapeBody(shape),'unbreakable')
-    end
-end
-
-
-GetCrosshairWorldPos = function(rejectBodies, fwdPos, pos)
-
-    for key, b in pairs(rejectBodies) do QueryRejectBody(b) end
-
-    local crosshairTr = GetCrosshairCameraTr()
-    if pos then
-        crosshairTr.pos = pos
-    end
-    local crosshairHit, crosshairHitPos = RaycastFromTransform(crosshairTr, 500)
-    if crosshairHit then
-        return crosshairHitPos
-    elseif not crosshairHit or fwdPos then
-        return TransformToParentPoint(GetCameraTransform(), Vec(0,0,-500))
-    end
-
-end
-
-
-GetCrosshairCameraTr = function(pos, x, y)
-
-    pos = pos or GetCameraTransform()
-
-    local crosshairDir = UiPixelToWorld(UiCenter(), UiMiddle())
-    local crosshairQuat = DirToQuat(crosshairDir)
-    local crosshairTr = Transform(GetCameraTransform().pos, crosshairQuat)
-
-    return crosshairTr
-
-end
-
-DebugPath = function(tb_points, tb_color, a, dots, dots_size)
-    if #tb_points >= 2 then
-        for i = 1, #tb_points - 1 do -- Stop at the second last point.
-            dbl(tb_points[i], tb_points[i+1], 1,1,1,1)
-            if dots then
-                DrawDot(tb_points[1], dots_size or 0.5, dots_size or 0.5, unpack(tb_color or Colors.white))
-                DrawDot(tb_points[#tb_points], dots_size or 0.5, dots_size or 0.5, unpack(tb_color or Colors.white))
-            end
-        end
-    end
-end
-
-
+#version 2
 function GetVecString(v)
     return (sfn(v[1]) .. ", " .. sfn(v[2]) .. ", " .. sfn(v[3]))
 end
 
---- Must be called in draw()
 function DebugCompass(font_size)
     UiPush()
 
@@ -347,7 +46,7 @@
     UiPop()
 end
 
-
 function IsInfrontOfTr(tr, pos)
     return TransformToLocalPoint(tr, pos)[3] < 0
-end+end
+

```

---

# Migration Report: TDSU\util_vfx.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/TDSU\util_vfx.lua
+++ patched/TDSU\util_vfx.lua
@@ -1,14 +1,3 @@
+#version 2
 function DrawDot(pos, l, w, r, g, b, a, dt) DrawImage("ui/hud/dot-small.png", pos, l, w, r, g, b, a, dt) end
 
--- function DrawUiDot(pos, size, r,g,b,a, safemode)
---     local x,y = UiWorldToPixel(pos)
---     UiPush()
---         if safemode then
---             UiColor(r or 1, g or 1, b or 1, a or 1)
---         end
---         UiImageBox("ui/common/dot.png", size, size, 0, 0)
---         UiTranslate(x,y)
---     UiPop()
--- end
-
--- function DrawBodyOutline() end

```
