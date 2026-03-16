# Migration Report: Automatic.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Automatic.lua
+++ patched/Automatic.lua
@@ -1,30 +1,11 @@
--- VERSION 1.10
--- I ask that you please do not rename Automatic.lua - Thankyou
-
--------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------Arithmetic Functions-------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------
-
----Logistic function, Can be used for juicy UI and smooth easing among other things.
----https://www.desmos.com/calculator/cmmwrjtyit?invertedColors
----@param v number|nil Input number, if nil then it will be a Random number between 0 and 1
----@param max number The Maximum value
----@param steep number How steep the curve is
----@param offset number The horizontal offset of the middle of the curve
----@return number
+#version 2
+local Stack = {}
+
 function AutoLogistic(v, max, steep, offset)
 	v = AutoDefault(v, math.random(0, 10000) / 10000)
 	return max / (1 + math.exp((v - offset) * steep))
 end
 
----Logistic function followed by a mapping function, guarantees that the return value will be between 0 and 1
----@param v number|nil Random number between 0 and 1
----@param max number The Maximum value
----@param steep number How steep the curve is
----@param offset number The horizontal offset of the middle of the curve
----@param rangemin number Maps this number to 0
----@param rangemax number Maps this numver to 1
----@return number
 function AutoLogisticScaled(v, max, steep, offset, rangemin, rangemax)
 	v = AutoLogistic(v, max, steep, offset)
 	local a = AutoLogistic(rangemin, max, steep, offset)
@@ -33,10 +14,6 @@
 	return AutoClamp(mapped, 0, 1)
 end
 
----This was a Challenge by @TallTim and @1ssnl to make the smallest rounding function, but I expanded it to make it easier to read and a little more efficent
----@param v number Input number
----@param increment number|nil The lowest increment. A Step of 1 will round the number to 1, A step of 5 will round it to the closest increment of 5, A step of 0.1 will round to the tenth. Default is 1
----@return number
 function AutoRound(v, increment)
 	increment = AutoDefault(increment, 1)
 	if increment == 0 then return v end
@@ -44,23 +21,11 @@
 	return math.floor(v * s + 0.5) / s
 end
 
----Maps a value from range a1-a2 to range b1-b2
----@param v number Input number
----@param a1 number Goes from the range of number a1
----@param a2 number To number a2
----@param b1 number To the range of b1
----@param b2 number To number b2
----@return number
 function AutoMap(v, a1, a2, b1, b2)
 	if a1 == a2 then return b2 end
 	return b1 + ((v - a1) * (b2 - b1)) / (a2 - a1)
 end
 
----Limits a value from going below the min and above the max
----@param v number The number to clamp
----@param min number|nil The minimum the number can be, Default is 0
----@param max number|nil The maximum the number can be, Default is 1
----@return number
 function AutoClamp(v, min, max)
 	min = AutoDefault(min, 0)
 	max = AutoDefault(max, 1)
@@ -73,11 +38,6 @@
 	end
 end
 
----Wraps a value inbetween a range
----@param v number The number to wrap
----@param min number|nil The minimum range
----@param max number|nil The maximum range
----@return number
 function AutoWrap(v, min, max)
 	min = AutoDefault(min, 0)
 	max = AutoDefault(max, 1)
@@ -87,20 +47,10 @@
 	return AutoMap(v, 0, 1, min, max)
 end
 
----Lerp function, Is not clamped meaning it if t is above 1 then it will 'overshoot'
----@param a number Goes from number A
----@param b number To number B
----@param t number Interpolated by T
----@return number
 function AutoLerpUnclamped(a, b, t)
 	return (1 - t) * a + t * b
 end
 
----Moves a towards b by t
----@param a number Goes from number A
----@param b number To number B
----@param t number Moved by T
----@return number
 function AutoMove(a, b, t)
 	output = a
 	if a == b then
@@ -114,22 +64,10 @@
 	return output
 end
 
----Return the Distance between the numbers a and b
----@param a number
----@param b number
----@return number
 function AutoDist(a, b)
 	return math.abs(a - b)
 end
 
--------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------Vector Functions-----------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------
-
----Return a Random Vector
----@param length number
----@param precision number|nil 0.001 by default
----@return table
 function AutoRndVec(length, precision)
 	precision = AutoDefault(precision, 0.01)
 	local m = 1/precision
@@ -137,29 +75,14 @@
 	return VecScale(v, length)	
 end
 
----Return the Distance between Two Vectors
----@param a Vec
----@param b Vec
----@return number
 function AutoVecDist(a, b)
 	return math.sqrt( (a[1] - b[1])^2 + (a[2] - b[2])^2 + (a[3] - b[3])^2 )
 end
 
----Return a vector that has the magnitude of b, but with the direction of a
----@param a Vec
----@param b number
----@return Vec
 function AutoVecRescale(a, b)
 	return VecScale(VecNormalize(a), b)
 end
 
----Maps a Vector from range a1-a2 to range b1-b2
----@param v Vec Input Vector
----@param a1 number Goes from the range of number a1
----@param a2 number To number a2
----@param b1 number To the range of b1
----@param b2 number To number b2
----@return Vec
 function AutoVecMap(v, a1, a2, b1, b2)
 	if a1 == a2 then return AutoVecRescale(v, b2) end
 	local out = {
@@ -170,11 +93,6 @@
 	return out
 end
 
----Limits the magnitude of a vector to be between min and max
----@param v Vec The Vector to clamp
----@param min number|nil The minimum the magnitude can be, Default is 0
----@param max number|nil The maximum the magnitude can be, Default is 1
----@return Vec
 function AutoVecClampMagnitude(v, min, max)
 	min, max = AutoDefault(min, 0), AutoDefault(max, 1)
 	local l = VecLength(v)
@@ -187,11 +105,6 @@
 	end
 end
 
----Limits a vector to be between min and max
----@param v Vec The Vector to clamp
----@param min number|nil The minimum, Default is 0
----@param max number|nil The maximum, Default is 1
----@return Vec
 function AutoVecClamp(v, min, max)
 	min, max = AutoDefault(min, 0), AutoDefault(max, 1)
 	return {
@@ -201,9 +114,6 @@
 	}
 end
 
----Return Vec(1, 1, 1) scaled by length
----@param length number return the vector of size length, Default is 1
----@return Vec
 function AutoVecOne(length)
 	return VecScale(Vec(1,1,1), length)
 end
@@ -212,10 +122,6 @@
 	return VecScale(VecAdd(a, b), 0.5)
 end
 
----Return Vec a multiplied by Vec b
----@param a Vec
----@param b Vec
----@return Vec
 function AutoVecMulti(a, b)
 	return {
 		a[1] * b[1],
@@ -224,10 +130,6 @@
 	}
 end
 
----Return Vec a divided by Vec b
----@param a Vec
----@param b Vec
----@return Vec
 function AutoVecDiv(a, b)
 	return {
 		a[1] / b[1],
@@ -236,10 +138,6 @@
 	}
 end
 
----Return Vec a to the Power of b
----@param a Vec
----@param b number
----@return Vec
 function AutoVecPow(a, b)
 	return {
 		a[1] ^ b,
@@ -248,10 +146,6 @@
 	}
 end
 
----Return Vec a to the Power of Vec b
----@param a Vec
----@param b Vec
----@return Vec
 function AutoVecPowVec(a, b)
 	return {
 		a[1] ^ b[1],
@@ -260,9 +154,6 @@
 	}
 end
 
----Return Vec Absoulte Value
----@param v Vec
----@return Vec
 function AutoVecAbs(v)
 	return {
 		math.abs(v[1]),
@@ -271,50 +162,26 @@
 	}
 end
 
----Equivalent to math.min(unpack(v))
----@param v Vec
----@return number
 function AutoVecMin(v)
 	return math.min(unpack(v))
 end
 
----Equivalent to math.max(unpack(v))
----@param v Vec
----@return number
 function AutoVecMax(v)
 	return math.max(unpack(v))
 end
 
----Return Vec v with it's x value replaced by subx
----@param v Vec
----@param subx number
 function AutoVecSubsituteX(v, subx)
 	return Vec(subx, v[2], v[3])
 end
 
----Return Vec v with it's y value replaced by suby
----@param v Vec
----@param suby number
 function AutoVecSubsituteY(v, suby)
 	return Vec(v[1], suby, v[3])
 end
 
----Return Vec v with it's z value replaced by subz
----@param v Vec
----@param subz number
 function AutoVecSubsituteZ(v, subz)
 	return Vec(v[1], v[2], subz)
 end
 
--------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------Bounds Functions-----------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------
-
----Takes two vectors and modifys them so they can be used in other bound functions
----@param aa Vec
----@param bb Vec
----@return Vec
----@return Vec
 function AutoBoundsCorrection(aa, bb)
 	local min, max = VecCopy(aa), VecCopy(bb)
 
@@ -334,11 +201,6 @@
 	return min, max
 end
 
----Get a position inside or on the Input Bounds
----@param aa Vec Minimum Bound Corner
----@param bb Vec Maximum Bound Corner
----@param vec Vec|nil A normalized Vector pointing towards the position that should be retrieved, Default is Vec(0, 0, 0)
----@return Vec
 function AutoBoundsGetPos(aa, bb, vec)
 	vec = AutoDefault(vec, Vec(0,0,0))
 
@@ -351,10 +213,6 @@
 	return VecAdd(scaled, aa)
 end
 
----Get the center of the faces of the given Bounds, as if it was a cube
----@param aa Vec Minimum Bound Corner
----@param bb Vec Maximum Bound Corner
----@return table
 function AutoBoundsGetFaceCenters(aa, bb)
 	aa, bb = AutoBoundsCorrection(aa, bb)
 	return {
@@ -367,10 +225,6 @@
 	}
 end
 
----Get the corners of the given Bounds
----@param aa Vec Minimum Bound Corner
----@param bb Vec Maximum Bound Corner
----@return table
 function AutoBoundsGetCorners(aa, bb)
 	aa, bb = AutoBoundsCorrection(aa, bb)
 	return {
@@ -385,12 +239,6 @@
 	}
 end
 
----Get data about the size of the given Bounds
----@param aa Vec Minimum Bound Corner
----@param bb Vec Maximum Bound Corner
----@return Vector representing the size of the Bounds
----@return the smallest edge size of the Bounds
----@return the longest edge size of the Bounds
 function AutoBoundsSize(aa, bb)
 	aa, bb = AutoBoundsCorrection(aa, bb)
 	local size = VecSub(bb, aa)
@@ -400,15 +248,6 @@
 	return size, minval, maxval
 end
 
----Draws the world space bounds between the given bounds
----@param aa Vec Minimum Bound Corner
----@param bb Vec Maximum Bound Corner
----@param rgbcolors boolean|nil If the Minimum and Maximum corners are colorcoded representing the xyz axis colors, Default is false
----@param hue number|nil 0 to 1 representing the hue of the lines, Default is 0
----@param saturation number|nil 0 to 1 representing the saturation of the lines, Default is 0
----@param value number|nil 0 to 1 representing the value of the lines, Default is 0
----@param alpha number|nil the alpha of the lines, Default is 1
----@param draw boolean|nil Whether to use DebugLine or DrawLine, Default is false (DebugLine)
 function AutoDrawBounds(aa, bb, rgbcolors, hue, saturation, value, alpha, draw)
 	aa, bb = AutoBoundsCorrection(aa, bb)
 	rgbcolors = AutoDefault(rgbcolors, false)
@@ -460,25 +299,6 @@
 	end
 end
 
--------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------Point Physics------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------
-
-AutoSimulation = {}
-AutoSimSettings = {
-	Gravity = -10,
-	Drag = 0.0,
-	PointsAffectBodies = true,
-}
-
----Creates a Point to be Simulated with AutoSimulatePoints(). After using AutoCreatePoint(), you can can also add parameters and change existing ones, such as point.reflectivity, and point.mass
----@param Position Vec|nil Default is Vec(0, 0, 0)
----@param Velocity Vec|nil Default is Vec(0, 0, 0)
----@param Radius number|nil Default is 0
----@param Collision boolean|nil If the point should check for collision. Default is true
----@param Simulated boolean|nil If the point is simulated. Default is true
----@return table point
----@return number index
 function AutoSimCreatePoint(Position, Velocity, Radius, Collision, Simulated)
 	local new_point = {}
 	new_point.pos = AutoDefault(Position, {0, 0, 0})
@@ -497,9 +317,6 @@
 	return new_point, new_index
 end
 
-
----Updates all of the point in the Simulation
----@param dt number The timestep that is used. Default is GetTimeStep()
 function AutoSimUpdate(dt)
 	dt = AutoDefault(dt, GetTimeStep())
 	
@@ -582,13 +399,6 @@
 	end
 end
 
--------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------Table Functions------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------
-
----Returns the amount of elements in the given list.
----@param t table
----@return integer
 function AutoTableCount(t)
 	local c = 0
 	for i in pairs(t) do
@@ -598,10 +408,6 @@
 	return c
 end
 
----Returns true and the index if the v is in t, otherwise returns false and nil
----@param t table
----@param v any
----@return boolean, unknown
 function AutoTableContains(t, v)
 	for i, v2 in ipairs(t) do
 		if v == v2 then
@@ -611,17 +417,10 @@
 	return false, nil
 end
 
----Returns the Last item of a given list
----@param t any
----@return unknown
 function AutoTableLast(t)
 	return t[AutoTableCount(t)]
 end
 
----Copy a Table Recursivly Stolen from http://lua-users.org/wiki/CopyTable
----@param orig table
----@param copies table
----@return table
 function AutoTableDeepCopy(orig, copies)
 	copies = copies or {}
 	local orig_type = type(orig)
@@ -643,30 +442,15 @@
 	return copy
 end
 
--------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------Utility Functions------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------
-
----If val is nil, return default instead
----@param v any
----@param default any
----@return any
 function AutoDefault(v, default)
 	if v == nil then return default else return v end
 end
 
----Returns a Vector for easy use when put into a parameter for xml
----@param vec any
----@param round number
----@return string
 function AutoVecToXML(vec, round)
 	round = AutoDefault(round, 0)
 	return AutoRound(vec[1], round) .. ' ' .. AutoRound(vec[2], round) .. ' ' .. AutoRound(vec[3], round)
 end
 
----A workaround to making a table readonly, don't use, it most likely is bugged in someway
----@param t table
----@return table
 function AutoSetReadOnly(t)
 	return setmetatable({}, {
 		__index = t,
@@ -676,9 +460,6 @@
 	})
 end
 
----Code donatated from @Dr. HypnoTox - Thankyou! Turns a Table into a string
----@param object any
----@return string
 function AutoToString(object)
 	if object == nil then
 		return 'nil'
@@ -711,10 +492,6 @@
 	return toDump
 end
 
----Splits a string by a separator
----@param inputstr string
----@param sep string
----@return table
 function AutoSplit(inputstr, sep)
 	if sep == nil then
 		sep = "%s"
@@ -726,11 +503,6 @@
 	return t
 end
 
----Create a Vector in RGB color space from HSV color values
----@param hue number|nil The hue, Default is 0
----@param sat number|nil The saturation, Default is 1
----@param val number|nil The value, Default is 1
----@return Vec
 function AutoHSVToRGB(hue, sat, val)
 	hue = AutoDefault(hue, 0)
 	sat = AutoDefault(sat, 1)
@@ -752,17 +524,6 @@
 	return out
 end
 
--------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------Game Functions-------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------
-
----Checks if a point is in the view using a transform acting as the "Camera"
----@param point Vec
----@param fromtrans Transfrom|nil The Transform acting as the camera, Default is the Player's Camera
----@param angle number|nil The Angle at which the point can be seen from, Default is the Player's FOV set in the options menu
----@param raycastcheck boolean|nil Check to make sure that the point is not obscured, Default is true
----@return boolean seen If the point is in View
----@return number angle The Angle the point is away from the center of the looking direction
 function AutoPointInView(point, fromtrans, angle, raycastcheck)
 	fromtrans = AutoDefault(fromtrans, GetCameraTransform())
 	angle = AutoDefault(angle, GetInt('options.gfx.fov'))
@@ -790,10 +551,6 @@
 	}
 end
 
----Get the last Path Query as a path of points
----@param precision number The Accuracy
----@return table
----@return Vec "Last Point"
 function AutoRetrievePath(precision)
 	precision = AutoDefault(precision, 0.2)
 
@@ -808,18 +565,12 @@
 	return path, path[#path]
 end
 
----Reject a table of bodies for the next Query
----@param bodies table
 function AutoQueryRejectBodies(bodies)
 	for i in pairs(bodies) do
 		QueryRejectBody(bodies[i])
 	end
 end
 
----Set the collision filter for the shapes owned by a body
----@param body number
----@param layer number
----@param masknummber number bitmask
 function AutoSetBodyCollisionFilter(body, layer, masknummber)
 	local shapes = GetBodyShapes(body)
 	for i in pairs(shapes) do
@@ -827,29 +578,16 @@
 	end
 end
 
----Get the Center of Mass of a body in World space
----@param body any
----@return table
 function AutoWorldCenterOfMass(body)
 	local trans = GetBodyTransform(body)
 	local pos = TransformToParentPoint(trans, GetBodyCenterOfMass(body))
 	return pos
 end
 
----Get the Total Speed of a body
----@param body number
----@return number
 function AutoSpeed(body)
 	return VecLength(GetBodyVelocity(body)) + VecLength(GetBodyAngularVelocity(body))
 end
 
----Attempt to predict the position of a body in time
----@param body number
----@param time number
----@param raycast boolean|nil Check and Halt on Collision, Default is false
----@return table log
----@return table vel
----@return table normal
 function AutoPredictPosition(body, time, raycast)
 	raycast = AutoDefault(raycast, false)
 	local pos = AutoWorldCenterOfMass(body)
@@ -872,17 +610,11 @@
 	return log, vel, normal
 end
 
----Attempt to predict the position of the player in time
----@param time number
----@param raycast boolean|nil Check and Halt on Collision, Default is false
----@return table log
----@return table vel
----@return table normal
 function AutoPredictPlayerPosition(time, raycast)
 	raycast = AutoDefault(raycast, false)
-	local player = GetPlayerTransform(true)
+	local player = GetPlayerTransform(playerId, true)
 	local pos = player.pos
-	local vel = GetPlayerVelocity()
+	local vel = GetPlayerVelocity(playerId)
 	local log = { VecCopy(pos) }
 	local normal = Vec(0, 1, 0)
 
@@ -903,28 +635,16 @@
 	return log, vel, normal
 end
 
--------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------Showing Debug-------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------
-
----A Alternative to DebugPrint that uses AutoToString(), works with tables. Returns the Input
----@param ... any
----@return unknown Arguments
 function AutoPrint(...)
 	arg.n = nil
 	DebugPrint(AutoToString(arg))
 	return unpack(arg)
 end
 
----Prints 24 blank lines to quote on quote, "clear the console"
 function AutoClearConsole()
 	for i = 1, 24 do DebugPrint('') end
 end
 
----Draws a table of 
----@param points any
----@param huescale number|nil A multipler to the hue change, Default is 1
----@param draw boolean|nil Whether to use DebugLine or DrawLine, Default is false (DebugLine)
 function AutoDrawLines(points, huescale, draw)
 	huescale = AutoDefault(huescale, 1)
 	draw = AutoDefault(draw, false)
@@ -947,11 +667,6 @@
 	end
 end
 
----Draws a Transform
----@param transform Transform
----@param size number the size in meters, Default is 0.5
----@param alpha number Default is 1
----@param draw boolean|nil Whether to use DebugLine or DrawLine, Default is false (DebugLine)
 function AutoDrawTransform(transform, size, alpha, draw)
 	transform.rot = AutoDefault(transform.rot, QuatEuler(0, 0, 0))
 	size = AutoDefault(size, 0.5)
@@ -977,9 +692,6 @@
 	end
 end
 
----Draws some Debug information about a body
----@param body number
----@param size number
 function AutoDrawBodyDebug(body, size)
 	local trans = GetBodyTransform(body)
 	AutoDrawTransform(trans, size)
@@ -990,12 +702,6 @@
 	AutoTooltip(AutoRound(AutoSpeed(body), 0.001), trans.pos, 16, 0.35)
 end
 
----Draws some text at a world position.
----@param text string
----@param position Vec
----@param fontsize number
----@param alpha number
----@param bold boolean
 function AutoTooltip(text, position, fontsize, alpha, bold)
 	text = AutoDefault(text or "nil")
 	fontsize = AutoDefault(fontsize or 24)
@@ -1023,16 +729,12 @@
 	UiPop()
 end
 
--------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------Registry-------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------
-
 function AutoKeyDefaultInt(path, default)
 	if path == nil then error("path nil") end
 	if HasKey(path) then
 		return GetInt(path)
 	else
-		SetInt(path, default)
+		SetInt(path, default, true)
 		return default
 	end
 end
@@ -1042,7 +744,7 @@
 	if HasKey(path) then
 		return GetFloat(path)
 	else
-		SetFloat(path, default)
+		SetFloat(path, default, true)
 		return default
 	end
 end
@@ -1052,27 +754,11 @@
 	if HasKey(path) then
 		return GetString(path)
 	else
-		SetString(path, default)
+		SetString(path, default, true)
 		return default
 	end
 end
 
--------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------User Interface-------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------
-
-AutoPad = {none = 0, atom = 4, micro = 6, thin = 12, thick = 24, heavy = 48, beefy = 128}
-setmetatable(AutoPad, { __call = function (t, padding) UiTranslate(padding, padding) end})
-
-AutoPrimaryColor = {0.95, 0.95, 0.95, 1}
-AutoSpecialColor = {1, 1, 0.55, 1}
-AutoSecondaryColor = {0, 0, 0, 0.55}
-AutoFont = 'regular.ttf'
-local Stack = {}
-
----Takes an alignment and returns a Vector representation.
----@param alignment string
----@return table
 function AutoAlignmentToPos(alignment)
 	v, y = 0, 0
 	if string.find(alignment, 'left') then v = -1 end
@@ -1084,49 +770,36 @@
 	return {x = v, y = y}
 end
 
----UiTranslate and UiAlign to the Center
 function AutoCenter()
 	UiTranslate(UiCenter(), UiMiddle())
 	UiAlign('center middle')
 end
 
----The next Auto Ui functions will be spread Down until AutoSpreadEnd() is called
----@param padding number|nil The amount of padding that will be used, Default is AutoPad.thin
 function AutoSpreadDown(padding)
 	table.insert(Stack, {type = 'spread', direction = 'down', padding = AutoDefault(padding, AutoPad.thin)})
 	UiPush()
 end
 
----The next Auto Ui functions will be spread Up until AutoSpreadEnd() is called
----@param padding number|nil The amount of padding that will be used, Default is AutoPad.thin
 function AutoSpreadUp(padding)
 	table.insert(Stack, {type = 'spread', direction = 'up', padding = AutoDefault(padding, AutoPad.thin)})
 	UiPush()
 end
 
----The next Auto Ui functions will be spread Right until AutoSpreadEnd() is called
----@param padding number|nil The amount of padding that will be used, Default is AutoPad.thin
 function AutoSpreadRight(padding)
 	table.insert(Stack, {type = 'spread', direction = 'right', padding = AutoDefault(padding, AutoPad.thin)})
 	UiPush()
 end
 
----The next Auto Ui functions will be spread Left until AutoSpreadEnd() is called
----@param padding number|nil The amount of padding that will be used, Default is AutoPad.thin
 function AutoSpreadLeft(padding)
 	table.insert(Stack, {type = 'spread', direction = 'left', padding = AutoDefault(padding, AutoPad.thin)})
 	UiPush()
 end
 
----The next Auto Ui functions will be spread Verticlely across the Height of the Bounds until AutoSpreadEnd() is called
----@param count number|nil The amount of Auto Ui functions until AutoSpreadEnd()
 function AutoSpreadVerticle(count)
 	table.insert(Stack, {type = 'spread', direction = 'verticle', length = UiHeight(), count = count})
 	UiPush()
 end
 
----The next Auto Ui functions will be spread Horizontally across the Width of the Bounds until AutoSpreadEnd() is called
----@param count number|nil The amount of Auto Ui functions until AutoSpreadEnd()
 function AutoSpreadHorizontal(count)
 	table.insert(Stack, { type = 'spread', direction = 'horizontal', length = UiWidth(), count = count })
 	UiPush()
@@ -1158,8 +831,6 @@
 	v = Spread
 end
 
----Stop the last known Spread
----@return table a table with information about the transformations used
 function AutoSpreadEnd()
 	local unitdata = {comb = { w = 0, h = 0 }, max = { w = 0, h = 0 }}
 	local Spread = AutoGetSpread()
@@ -1210,17 +881,7 @@
 		table.insert(Stack, { type = type, data = data })
 	end
 end
--------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------User Interface Creation Functions-------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------
-
----Create a Container with new bounds
----@param width number
----@param height number
----@param padding number|nil The Amount of padding against sides of the container, Default is AutoPad.micro
----@param clip boolean|nil Whether  to clip stuff outside of the container, Default is false
----@param draw boolean|nil Draws the container's background, otherwise it will be invisible, Defualt is true
----@return table containerdata
+
 function AutoContainer(width, height, padding, clip, draw)
 	width = AutoDefault(width, 300)
 	height = AutoDefault(height, 400)
@@ -1254,15 +915,6 @@
 	return { rect = { w = paddingwidth, h = paddingheight }, hover = hover }
 end
 
----Creates a Button
----@param name string
----@param fontsize number
----@param paddingwidth number Amount of padding used Horizontally
----@param paddingheight number Amount of padding used Vertically
----@param draw boolean Draws the Button
----@param spreadpad boolean Adds padding when used with AutoSpread...()
----@return boolean Pressed
----@return table ButtonData
 function AutoButton(name, fontsize, paddingwidth, paddingheight, draw, spreadpad)
 	fontsize = AutoDefault(fontsize, 28)
 	paddingwidth = AutoDefault(paddingwidth, AutoPad.thick)
@@ -1296,16 +948,6 @@
 	return pressed, data
 end
 
-
----Creates a Button
----@param name string
----@param fontsize number
----@param paddingwidth number Amount of padding used Horizontally
----@param paddingheight number Amount of padding used Vertically
----@param draw boolean Draws the Button
----@param spreadpad boolean Adds padding when used with AutoSpread...()
----@return boolean Pressed
----@return table ButtonData
 function AutoToggleButton(bool, name, fontsize, paddingwidth, paddingheight, draw, spreadpad)
 	fontsize = AutoDefault(fontsize, 28)
 	paddingwidth = AutoDefault(paddingwidth, AutoPad.thick)
@@ -1356,13 +998,6 @@
 
 end
 
-
----Draws some Text
----@param name string
----@param fontsize number
----@param draw boolean Draws the Text
----@param spreadpad boolean Adds padding when used with AutoSpread...()
----@return table TextData
 function AutoText(name, fontsize, draw, spreadpad)
 	fontsize = AutoDefault(fontsize, 28)
 	draw = AutoDefault(draw, true)
@@ -1392,16 +1027,6 @@
 	return data
 end
 
----Creates a Slider
----@param set number The Current Value
----@param min number The Minimum
----@param max number The Maximum
----@param lockincrement number The increment
----@param paddingwidth Amount of padding used Horizontally
----@param paddingheight Amount of padding used Vertically
----@param spreadpad boolean Adds padding when used with AutoSpread...()
----@return number NewValue
----@return table SliderData
 function AutoSlider(set, min, max, lockincrement, paddingwidth, paddingheight, spreadpad)
 	min = AutoDefault(min, 0)
 	max = AutoDefault(max, 1)
@@ -1440,14 +1065,6 @@
 	return set, data
 end
 
----Draws an Image
----@param path string
----@param width number
----@param height number
----@param alpha number
----@param draw boolean Draws the Image
----@param spreadpad boolean Adds padding when used with AutoSpread...()
----@return table ImageData
 function AutoImage(path, width, height, alpha, draw, spreadpad)
 	local w, h = UiGetImageSize(path)
 	width = AutoDefault(width, (height == nil and UiWidth() or (height * (w / h))))
@@ -1471,8 +1088,6 @@
 	return data
 end
 
----Creates a handy little marker, doesnt effect anything, purely visual
----@param size number, Default is 1
 function AutoMarker(size)
 	size = AutoDefault(size, 1) / 2
 	UiPush()
@@ -1481,4 +1096,5 @@
 		UiColor(unpack(AutoSpecialColor))
 		UiImage('ui/common/dot.png')
 	UiPop()
-end+end
+

```

---

# Migration Report: custom_robot\main\mapScript.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_robot\main\mapScript.lua
+++ patched/custom_robot\main\mapScript.lua
@@ -1,3 +1,5 @@
-function init()
-    SetBool('LEVEL.demoMap', true)
+#version 2
+function server.init()
+    SetBool('LEVEL.demoMap', true, true)
 end
+

```

---

# Migration Report: custom_robot\scripts\camera.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_robot\scripts\camera.lua
+++ patched/custom_robot\scripts\camera.lua
@@ -1,46 +1 @@
-initCamera = function()
-	cameraX = 0
-	cameraY = 0
-	zoom = 2
-end
-
-manageCamera = function(disableRotation, height)
-	local mx, my = InputValue("mousedx"), InputValue("mousedy")
-	disableRotation = disableRotation or false
-	if disableRotation then mx, my = 0,0 end
-	cameraX = cameraX - mx / 10
-	cameraY = cameraY - my / 10
-	cameraY = clamp(cameraY, -75, 75)
-	local cameraRot = QuatEuler(cameraY, cameraX, 0)
-	local cameraT = Transform(VecAdd(GetBodyTransform(robot.body).pos, 5), cameraRot)
-	zoom = zoom - InputValue("mousewheel") * 2.5
-	zoom = clamp(zoom, 2, 20)
-	local cameraPos = TransformToParentPoint(cameraT, Vec(0, height + zoom/10, zoom))
-	local camera = Transform(VecLerp(cameraPos, GetCameraTransform().pos, 0.5), cameraRot)
-	SetCameraTransform(camera)
-end
-
-getOuterCrosshairWorldPos = function()
-
-	local crosshairTr = getCrosshairTr()
-	rejectAllBodies(robot.allBodies)
-	local crosshairHit, crosshairHitPos = RaycastFromTransform(crosshairTr, 200)
-	if crosshairHit then
-		return crosshairHitPos
-	else
-		return nil
-	end
-
-end
-
-getCrosshairTr = function(pos)
-
-	pos = pos or GetCameraTransform()
-
-	local crosshairDir = UiPixelToWorld(CAMERA.xy[1], CAMERA.xy[2])
-	local crosshairQuat = DirToQuat(crosshairDir)
-	local crosshairTr = Transform(GetCameraTransform().pos, crosshairQuat)
-
-	return crosshairTr
-
-end+#version 2

```

---

# Migration Report: custom_robot\scripts\customRobot.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_robot\scripts\customRobot.lua
+++ patched/custom_robot\scripts\customRobot.lua
@@ -1,10 +1,4 @@
---================================
---= Robot Vehicles
---= By: Cheejins
---================================
-
-
---> SCRIPT
+#version 2
 function initCustom()
 
 	CAMERA = {}
@@ -36,6 +30,7 @@
 	end
 
 end
+
 function tickCustom(dt)
 
 	--+ Global robot variables.
@@ -63,6 +58,7 @@
 	end
 
 end
+
 function updateCustom(dt)
 	robot.speedScale = regGetFloat('robot.move.speed')
 	timers.gun.bullets.rpm = regGetFloat('robot.weapon.bullet.rpm')
@@ -74,12 +70,13 @@
 
 	-- elseif regGetBool('robot.followPlayer') then
 
-	-- 	if VecDist(GetPlayerTransform().pos, robot.transform.pos) > 3 then
+	-- 	if VecDist(GetPlayerTransform(playerId).pos, robot.transform.pos) > 3 then
 	-- 		robotFollowPlayer(dt)
 	-- 	end
 
 	end
 end
+
 function drawCustom()
 
 	if player.isDrivingRobot and robot.enabled then
@@ -129,7 +126,7 @@
 				if InputPressed('any') then
 					enterCount = enterCount + 1
 					if enterCount > 1 then
-						SetBool('LEVEL.welcome', true)
+						SetBool('LEVEL.welcome', true, true)
 					end
 				end
 
@@ -140,79 +137,6 @@
 
 end
 
-
-
---> MOVEMENT
-processMovement = function ()
-
-	-- navigationClear()
-
-	local walk = false
-	local walkDir = Vec()
-	local lookTr = Transform(robot.transform.pos, camTr.rot)
-
-	--+ WASD
-	if InputDown('up') then
-		local moveDir = TransformToParentVec(lookTr, Vec(0,0,-1))
-		walkDir = VecAdd(walkDir, moveDir)
-		walk = true
-	elseif InputDown('down') then
-		local moveDir = TransformToParentVec(lookTr, Vec(0,0,1))
-		walkDir = VecAdd(walkDir, moveDir)
-		walk = true
-	end
-
-	if InputDown('left') then
-		local moveDir = TransformToParentVec(lookTr, Vec(-1,0,0))
-		walkDir = VecAdd(walkDir, moveDir)
-		walk = true
-	end
-	if InputDown('right') then
-		local moveDir = TransformToParentVec(lookTr, Vec(1,0,0))
-		walkDir = VecAdd(walkDir, moveDir)
-		walk = true
-	end
-
-	if walk then
-		walkDir = VecNormalize(walkDir)
-		robotWalk(walkDir)
-	end
-
-	--+ Sprint
-	if InputDown('shift') then
-		robot.speedScale = regGetFloat('robot.move.speed') * 2
-	else
-		robot.speedScale = regGetFloat('robot.move.speed')
-	end
-
-	--+ Jump
-	if InputPressed('space') then
-		SetBodyVelocity(robot.body, VecAdd(GetBodyVelocity(robot.body), Vec(0,10,0)))
-	end
-
-	--+ Crouch
-	if InputPressed('ctrl') then
-		SetBodyVelocity(robot.body, VecAdd(GetBodyVelocity(robot.body), Vec(0,-5,0)))
-		-- DebugPrint('Teabag initiated ' .. sfnTime())
-	end
-
-end
-robotWalk = function (robotDir)
-	robot.dir = robotDir
-	local dirDiff = VecDot(VecScale(robot.axes[3], -1), robot.dir)
-	local speedScale = math.max(0.25, dirDiff)
-	speedScale = speedScale * clamp(1.0 - navigation.vertical, 0.3, 1.0)
-	robot.speed = config.speed * speedScale
-end
-robotFollowPlayer = function(dt)
-	navigationSetTarget(GetPlayerTransform().pos, 5)
-	navigationMove(dt)
-	navigationUpdate(dt)
-end
-
-
-
---> WEAPONS
 function processWeapons()
 
 	if robot.model == robot_models.basic then
@@ -222,6 +146,7 @@
 	end
 
 end
+
 function processWeapons_mech_aeon()
 
 	-- Draw dots at shooting positions.
@@ -255,7 +180,6 @@
 				-- Shoot projectile.
 				createProjectile(shootTr, Projectiles, ProjectilePresets.aeon_secondary, robot.allBodies)
 
-
 				-- Apply recoil,
 				local vel_impulse = VecScale(QuatToDir(weapTr.rot), -4500)
 				ApplyBodyImpulse(robot.body, AabbGetBodyCenterPos(robot.body), vel_impulse)
@@ -301,6 +225,7 @@
 	end
 
 end
+
 function processWeapons_mech_basic()
 	-- Bullets
 	if InputDown('lmb') then
@@ -342,9 +267,6 @@
 			rejectAllBodies(robot.allBodies)
 			createBullet(leftTr, activeBullets, bulletPresets.mg.light, robot.allBodies)
 
-
-
-
 			local rightTr = Transform(TransformToParentPoint(shootTr, Vec(0.5, 0, 0)), shootTr.rot)
 			rightTr = Transform(rightTr.pos, QuatLookAt(rightTr.pos, TransformToParentPoint(rightTr, Vec(0,0,-1))))
 
@@ -413,6 +335,7 @@
 
 	end
 end
+
 function aimsUpdateCustom()
 	for i=1, #aims do
 		local aim = aims[i]
@@ -436,20 +359,14 @@
 	end
 end
 
-
-
---> PLAYER
-player = {}
-player.isDrivingRobot = false
 function playerDriveRobot(dt, pos)
 
 	--+ Update player values.
-	SetPlayerTransform(Transform(pos))
-	SetPlayerHealth(1)
-	SetString("game.player.tool", 'sledge')
-	SetPlayerVelocity(Vec())
+	SetPlayerTransform(playerId, Transform(pos))
+	SetPlayerHealth(playerId, 1)
+	SetString("game.player.tool", 'sledge', true)
+	SetPlayerVelocity(playerId, Vec())
 	SetPlayerGroundVelocity(Vec())
-
 
 	manageCamera(UI_OPTIONS, robot.cameraHeight)
 
@@ -468,6 +385,7 @@
 	end
 
 end
+
 function playerCheckRobot()
 
 	if robot.enabled then
@@ -478,13 +396,13 @@
 			if InputPressed('interact') or InputPressed('e') then
 				player.isDrivingRobot = false
 				local playerExitTr = Transform(TransformToParentPoint(bodyTr, Vec(0,0,-2)))
-				SetPlayerTransform(playerExitTr)
+				SetPlayerTransform(playerId, playerExitTr)
 			end
 
 		elseif InputPressed('interact') or InputPressed('e') then
 
 			--+ Enter robot.
-			if GetPlayerInteractBody() == Eyes.body then
+			if GetPlayerInteractBody(playerId) == Eyes.body then
 				player.isDrivingRobot = true
 			end
 
@@ -498,18 +416,16 @@
 	else
 
 		player.isDrivingRobot = false
-		SetBool('level.playerIsDrivingRobot', false)
-
-	end
-
-end
-
-
-
---> OTHER
+		SetBool('level.playerIsDrivingRobot', false, true)
+
+	end
+
+end
+
 function debugRobot()
 	dbw('model', robot.model)
 end
+
 function setRobotUnbreakable(setUnbreakable)
 
 	local func_setter
@@ -536,18 +452,20 @@
 	end
 
 end
+
 function initPlayerDrivingRobot()
 
 	-- if GetBool('level.robotExists') then
 
 	-- 	if not GetBool('level.playerIsDrivingRobot') then
 	-- 		-- player.isDrivingRobot = true
-	-- 		SetBool('level.playerIsDrivingRobot', true)
+	-- 		SetBool('level.playerIsDrivingRobot', true, true)
 	-- 	end
 
 	-- end
 
 end
+
 function manageRobotHealth()
 
 	-- if robot.enabled and getRobotMass() < robot.health*0.9 then
@@ -581,6 +499,7 @@
 	-- end
 
 end
+
 function getRobotMass()
 	local mass = 0
 	for key, body in pairs(robot.allBodies) do
@@ -589,3 +508,4 @@
 	end
 	return mass
 end
+

```

---

# Migration Report: custom_robot\scripts\debug.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_robot\scripts\debug.lua
+++ patched/custom_robot\scripts\debug.lua
@@ -1,15 +1,22 @@
+#version 2
 function initDebug()
     db = false
     -- db = true
 end
 
 function dbw(str, value) if db then DebugWatch(str, value) end end
+
 function dbp(str, newLine) if db then DebugPrint(str .. ternary(newLine, '\n', '')) print(str .. ternary(newLine, '\n', '')) end end
+
 function dbl(p1, p2, c1, c2, c3, a) if db then DebugLine(p1, p2, c1, c2, c3, a) end end
+
 function dbdd(pos,w,l,r,g,b,a,dt) DrawDot(pos,w,l,r,g,b,a,dt) end
 
---[[DEBUG 3D]]
-function dbl(p1, p2, r,g,b,a, dt) if db then DebugLine(p1, p2, r,g,b,a, dt) end end -- DebugLine()
-function dbdd(pos, w,l, r,g,b,a, dt) if db then DrawDot(pos,w,l,r,g,b,a,dt) end end -- Draw a dot sprite at the specified position.
-function dbray(tr, dist, r,g,b,a) dbl(tr.pos, TransformToParentPoint(tr, Vec(0,0,-dist)), r, g, b, a) end -- Debug a ray segement from a transform.
-function dbcr(pos, r,g,b, a) if db then DebugCross(pos, r or 1, g or 1, b or 1, a or 1) end end -- DebugCross() at a specified position.
+function dbl(p1, p2, r,g,b,a, dt) if db then DebugLine(p1, p2, r,g,b,a, dt) end end
+
+function dbdd(pos, w,l, r,g,b,a, dt) if db then DrawDot(pos,w,l,r,g,b,a,dt) end end
+
+function dbray(tr, dist, r,g,b,a) dbl(tr.pos, TransformToParentPoint(tr, Vec(0,0,-dist)), r, g, b, a) end
+
+function dbcr(pos, r,g,b, a) if db then DebugCross(pos, r or 1, g or 1, b or 1, a or 1) end end
+

```

---

# Migration Report: custom_robot\scripts\particles.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_robot\scripts\particles.lua
+++ patched/custom_robot\scripts\particles.lua
@@ -1,4 +1,4 @@
-
+#version 2
 function manageAeonWeaponParticles(proj)
 
     local trAhead = Transform(TransformToParentPoint(proj.transform, Vec(0,0,-proj.speed/1 + math.random())), proj.transform.rot)
@@ -15,8 +15,6 @@
 
 end
 
-
--- Aeon secondary
 function SpawnParticle_aeon_weap_secondary(tr, rad)
     local radius = rad or 0.5
     local life = 1.2
@@ -38,7 +36,6 @@
     ParticleDrag(drag)
     ParticleColor(red, green, blue, 0.0+ math.random()/10, 0.2+ math.random()/10, 0.6+ math.random()/10)			-- Animating color towards white
     ParticleEmissive(emissive, emissive/3, 'smooth', 0, 2)
-
 
     local p = tr.pos
     local v = VecAdd(VecScale(QuatToDir(tr.rot), vel), VecRdm(1))
@@ -70,14 +67,12 @@
     ParticleColor(red, green, blue, 1,1,1)			-- Animating color towards white
     ParticleEmissive(emissive, emissive/2, 'smooth', 0, 1)
 
-
     local p = tr.pos
     local v = VecAdd(VecScale(QuatToDir(tr.rot), vel), VecRdm(1))
     local l = rnd(life*0.5, life*1.5)
 
     SpawnParticle(p, v, l)
 end
-
 
 function SpawnParticle_aeon_weap_secondary_exhaust(tr, vel)
     local radius = 0.2
@@ -104,3 +99,4 @@
 
     SpawnParticle(p, v, l)
 end
+

```

---

# Migration Report: custom_robot\scripts\projectiles.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_robot\scripts\projectiles.lua
+++ patched/custom_robot\scripts\projectiles.lua
@@ -1,6 +1,4 @@
-Projectiles = {}
-
-
+#version 2
 function createProjectile(transform, projectiles, projPreset, ignoreBodies) --- Instantiates a proj and adds it to the projectiles table.
 
     local proj = DeepCopy(projPreset)
@@ -11,7 +9,7 @@
     trDir = VecNormalize(VecAdd(trDir, VecRdm(proj.spread)))
     proj.transform.rot = DirToQuat(trDir)
 
-    if proj.homing.max > 0 then
+    if proj.homing.max ~= 0 then
         local hit, pos = RaycastFromTransform(GetCameraTransform())
         local vecRdm = VecRdm(2)
         vecRdm[2] = 0
@@ -69,10 +67,10 @@
     local rcHit, hitPos, hitShape = RaycastFromTransform(proj.transform, proj.speed, proj.rcRad, proj.ignoreBodies, nil, true)
     if rcHit and not proj.hitInitial then
 
-        SetInt('level.destructible-bot.hitCounter', GetInt('level.destructible-bot.hitCounter') + 1)
-        SetInt('level.destructible-bot.hitShape',hitShape)
-        SetString('level.destructible-bot.weapon',"robotname")
-        SetFloat('level.destructible-bot.damage',damage)
+        SetInt('level.destructible-bot.hitCounter', GetInt('level.destructible-bot.hitCounter') + 1, true)
+        SetInt('level.destructible-bot.hitShape',hitShape, true)
+        SetString('level.destructible-bot.weapon',"robotname", true)
+        SetFloat('level.destructible-bot.damage',damage, true)
 
         proj.hitInitial = true
         proj.hit = true
@@ -80,7 +78,7 @@
         --+ Hit Action
         ApplyBodyImpulse(GetShapeBody(hitShape), hitPos, VecScale(QuatToDir(proj.transform.rot), proj.force))
 
-        if proj.explosionSize > 0 then
+        if proj.explosionSize ~= 0 then
             Explosion(hitPos, proj.explosionSize)
         end
 
@@ -220,3 +218,4 @@
 
     }
 end
+

```

---

# Migration Report: custom_robot\scripts\registry.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_robot\scripts\registry.lua
+++ patched/custom_robot\scripts\registry.lua
@@ -1,30 +1,23 @@
-MOD_VERSION = {
-    '2021-Dec-16',
-    '22.02.18',
-    '22.02.22',
-    '04.09.22',
-}
-
+#version 2
 function modReset()
 
-    regSetString('version'                          , GetModVersion())
+    regSetString('version'                          , GetModVersion(), true)
 
-    regSetFloat('robot.weapon.bullet.rpm'           , 800)
-    regSetFloat('robot.weapon.bullet.holeSize'      , 0.5)
-    regSetFloat('robot.weapon.rocket.rpm'           , 160)
-    regSetFloat('robot.weapon.rocket.explosionSize' , 1.5)
+    regSetFloat('robot.weapon.bullet.rpm'           , 800, true)
+    regSetFloat('robot.weapon.bullet.holeSize'      , 0.5, true)
+    regSetFloat('robot.weapon.rocket.rpm'           , 160, true)
+    regSetFloat('robot.weapon.rocket.explosionSize' , 1.5, true)
 
-    regSetFloat('robot.move.speed'                  , 1)
+    regSetFloat('robot.move.speed'                  , 1, true)
 
 end
 
-
 function optionsReset()
     activeAssignment = false
-    regSetString('options.keys.optionsScreen', 'o')
-    regSetString('options.keys.welcomeScreen', 'i')
-    regSetString('options.keys.spawnMenu', 'h')
-    regSetString('options.keys.quickSpawn', 'g')
+    regSetString('options.keys.optionsScreen', 'o', true)
+    regSetString('options.keys.welcomeScreen', 'i', true)
+    regSetString('options.keys.spawnMenu', 'h', true)
+    regSetString('options.keys.quickSpawn', 'g', true)
 end
 
 function checkRegInitialized()
@@ -37,10 +30,10 @@
 
         if version ~= regVersion then
             print('> Mod updated from ' .. regGetString('version') .. ' to ' .. GetModVersion())
-            regSetString('version', GetModVersion())
+            regSetString('version', GetModVersion(), true)
         end
 
-        regSetBool('regInit', true)
+        regSetBool('regInit', true, true)
         modReset()
         optionsReset()
 
@@ -56,23 +49,29 @@
     local p = 'savegame.mod.' .. path
     return GetFloat(p)
 end
-function regSetFloat(path, value)
+
+function regSetFloat(path, value, true)
     local p = 'savegame.mod.' .. path
-    SetFloat(p, value)
+    SetFloat(p, value, true)
 end
+
 function regGetBool(path)
     local p = 'savegame.mod.' .. path
     return GetBool(p)
 end
-function regSetBool(path, value)
+
+function regSetBool(path, value, true)
     local p = 'savegame.mod.' .. path
-    SetBool(p, value)
+    SetBool(p, value, true)
 end
+
 function regGetString(path)
     local p = 'savegame.mod.' .. path
     return GetString(p)
 end
-function regSetString(path, value)
+
+function regSetString(path, value, true)
     local p = 'savegame.mod.' .. path
-    SetString(p, value)
+    SetString(p, value, true)
 end
+

```

---

# Migration Report: custom_robot\scripts\robot.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_robot\scripts\robot.lua
+++ patched/custom_robot\scripts\robot.lua
@@ -1,2303 +1 @@
-#include "camera.lua"
-#include "customRobot.lua"
-#include "debug.lua"
-#include "particles.lua"
-#include "projectiles.lua"
-#include "registry.lua"
-#include "robotPreset.lua"
-#include "script/common.lua"
-#include "sounds.lua"
-#include "timers.lua"
-#include "ui.lua"
-#include "ui_components.lua"
-#include "umf.lua"
-#include "utility.lua"
-#include "version.lua"
-#include "weapons.lua"
-
-
---= ROBOT OVERVIEW
-do
---[[
-
-	The robot script should be parent of all bodies that make up the robot.
-	Configure the robot with the type parameter that can be combinations of the following words: --? Type Parameter
-
-		investigate:
-			investigate sounds in the environment
-		chase:
-			chase player when seen, this is the most common configuration
-		nooutline:
-			no outline when close and hidden
-		alarm:
-			trigger alarm when player is seen and lit by light for 2.0 seconds
-		stun:
-			electrocute player when close or grabbed
-		avoid:
-			avoid player (should not be combined chase, requires patrol locations)
-		aggressive:
-			always know where player is (even through walls)
-
-
-
-	The following robot parts are supported:
-
-		--* REQUIRED
-		body
-			(type body: required)
-			This is the main part of the robot and should be the --! heaviest part
-		head
-			(type body: required)
-			The head should be --! jointed to the body
-			(hinge joint with or without limits).
-			heardist=<value> - Maximum hearing distance in meters, default 100
-		eye
-			(type light: required)
-			Represents robot vision. The direction of light source determines what the robot can see.
-			--! Can be placed on head or body
-			viewdist=<value> - View distance in meters. Default 25.
-			viewfov=<value> - View field of view in degrees. Default 150.
-
-
-		--* OPTIONAL
-		aim
-			(type body: optional)
-			This part will be directed towards the player when seen and is usually equipped with weapons.
-			Should be jointed to body or head with ball joint. There can be multiple aims.
-
-		wheel
-			(type body: optional, should be static with no collisions)
-			If present --! wheels will rotate along with the motion of the robot.
-			There can be multiple wheels.
-
-		leg
-			(type body: optional)
-			Legs should be --! jointed between body and feet.
-			All legs will have collisions disabled when walking and enabled in rag doll mode. --! Legs no collision
-			There can be --! multiple legs.
-
-		foot
-			(type body: optional)
-			Foot bodies are --! animated with respect to the body when walking.
-			They only collide with the environment in rag doll mode.
-			tag force - --! Movement force scale, default is 1.
-			Can also be two values to separate linear and angular, for example: 2,0.5
-
-		weapon
-			(type location: optional)
-			Usually placed on aim head or body.
-			There are several types of weapons:
-			weapon		=	 fire 			- Emit fire when player is close and seen
-			weapon		=	 gun 			- Regular shot
-			weapon		=	 rocket 		- Fire rockets
-			strength	=	 <value> 		- The scaling factor which controls how much damage it makes (default is 1.0)
-
-			The following tags are used to control the --! weapon behavior
-			(only affect gun and rocket):
-			idle		=	 <seconds> 		- Idle time in between rounds
-			charge		=	 <seconds> 		- Charge time before firing
-			cooldown	=	 <seconds> 		- Cooldown between each shot in a round
-			count		=	 <number> 		- Number of shots in a round
-			spread		=	 <fraction> 	- How much each shot may deviates from optimal direction (for instance: 0.05 to deviate up to 5%)
-			maxdist		=	 <meters> 		- How far away target can be to trigger shot. Default is 100
-
-		patrol
-			(type location: optional)
-			If present the robot will patrol these locations.
-			Make sure to place near walkable ground.
-			Targets are visited in the --! same order they appear in scene explorer.
-			Avoid type robots MUST have patrol targets.
-
-		roam
-			(type trigger: optional)
-			If there are no patrol locations, the robot will --! roam randomly within this trigger.
-
-		limit
-			(type trigger: optional)
-			If present the robot will try stay within this trigger volume.
-			If robot ends up outside trigger, it will --! automatically navigate back inside.
-
-		investigate
-			(type trigger: optional)
-			If present and the robot has type investigate it will --! only react to sounds within this trigger.
-
-		activate
-			(type trigger: optional)
-			If present, robot will start inactive and --! become activated when player enters trigger
-
-]]
-end
-
-
-
---= MAIN
-do
-	--> Script
-	do
-
-		function init()
-			configInit()
-			robotInit()
-			hoverInit()
-			headInit()
-			sensorInit()
-			wheelsInit()
-			feetInit()
-			aimsInit()
-			weaponsInit()
-			navigationInit()
-			hearingInit()
-			stackInit()
-
-			--> Sound
-			patrolLocations = FindLocations("patrol")
-			shootSound = LoadSound("tools/gun0.ogg", 8.0)
-			rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
-			local nomDist = 7.0
-			if config.stepSound == "s" then nomDist = 5.0 end
-			if config.stepSound == "l" then nomDist = 9.0 end
-			stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
-			headLoop = LoadLoop("robot/head-loop.ogg", 7.0)
-			turnLoop = LoadLoop("robot/turn-loop.ogg", 7.0)
-			walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
-			rollLoop = LoadLoop("robot/roll-loop.ogg", 7.0)
-			chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
-			alertSound = LoadSound("robot/alert.ogg", 9.0)
-			huntSound = LoadSound("robot/hunt.ogg", 9.0)
-			idleSound = LoadSound("robot/idle.ogg", 9.0)
-			fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
-			disableSound = LoadSound("robot/disable0.ogg")
-
-			initCustom() --!
-
-		end
-
-		function update(dt)
-			if robot.deleted then
-				return
-			else
-				if not IsHandleValid(robot.body) then
-					for i=1, #robot.allBodies do
-						Delete(robot.allBodies[i])
-					end
-					for i=1, #robot.allJoints do
-						Delete(robot.allJoints[i])
-					end
-					robot.deleted = true
-				end
-			end
-
-			if robot.activateTrigger ~= 0 then
-				if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform().pos) then
-					RemoveTag(robot.body, "inactive")
-					robot.activateTrigger = 0
-				end
-			end
-
-			if HasTag(robot.body, "inactive") then
-				robot.inactive = true
-				return
-			else
-				if robot.inactive then
-					robot.inactive = false
-					--Reset robot pose
-					local sleep = HasTag(robot.body, "sleeping")
-					for i=1, #robot.allBodies do
-						SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
-						SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
-						SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
-						if sleep then
-							--If robot is sleeping make sure to not wake it up
-							SetBodyActive(robot.allBodies[i], false)
-						end
-					end
-				end
-			end
-
-			if HasTag(robot.body, "sleeping") then
-				if IsBodyActive(robot.body) then
-					wakeUp = true
-				end
-				local vol, pos = GetLastSound()
-				if vol > 0.2 then
-					if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
-						wakeUp = true
-					end
-				end
-				if wakeUp then
-					RemoveTag(robot.body, "sleeping")
-				end
-				return
-			end
-
-			robotUpdate(dt)
-			wheelsUpdate(dt)
-
-			if not robot.enabled then
-				return
-			end
-
-			feetUpdate(dt)
-
-			if IsPointInWater(robot.bodyCenter) then
-				PlaySound(disableSound, robot.bodyCenter)
-				for i=1, #robot.allShapes do
-					SetShapeEmissiveScale(robot.allShapes[i], 0)
-				end
-				SetTag(robot.body, "disabled")
-				robot.enabled = false
-			end
-
-			robot.stunned = clamp(robot.stunned - dt, 0.0, 8.0)
-			if robot.stunned > 0 then
-				Eyes.seenTimer = 0
-				weaponsReset()
-				return
-			end
-
-			hoverUpdate(dt)
-			headUpdate(dt)
-			sensorUpdate(dt)
-			aimsUpdate(dt)
-			weaponsUpdate(dt)
-			hearingUpdate(dt)
-			stackUpdate(dt)
-			robot.speedScale = 1.5
-			robot.speed = 0
-			-- local state = stackTop()
-			local state = "none"
-
-			if state.id == "none" then
-				-- if config.patrol then
-				-- 	stackPush("patrol")
-				-- else
-				-- 	stackPush("roam")
-				-- end
-			end
-
-			if state.id == "roam" then
-				-- if not state.nextAction then
-				-- 	state.nextAction = "move"
-				-- elseif state.nextAction == "move" then
-				-- 	local randomPos
-				-- 	if robot.roamTrigger ~= 0 then
-				-- 		randomPos = getRandomPosInTrigger(robot.roamTrigger)
-				-- 		randomPos = truncateToGround(randomPos)
-				-- 	else
-				-- 		local rndAng = rnd(0, 2*math.pi)
-				-- 		randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
-				-- 	end
-				-- 	local s = stackPush("navigate")
-				-- 	s.timeout = 1
-				-- 	s.pos = randomPos
-				-- 	state.nextAction = "search"
-				-- elseif state.nextAction == "search" then
-				-- 	stackPush("search")
-				-- 	state.nextAction = "move"
-				-- end
-			end
-
-
-			if state.id == "patrol" then
-				-- if not state.nextAction then
-				-- 	state.index = getClosestPatrolIndex()
-				-- 	state.nextAction = "move"
-				-- elseif state.nextAction == "move" then
-				-- 	markPatrolLocationAsActive(state.index)
-				-- 	local nav = stackPush("navigate")
-				-- 	nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
-				-- 	state.nextAction = "search"
-				-- elseif state.nextAction == "search" then
-				-- 	stackPush("search")
-				-- 	state.index = getNextPatrolIndex(state.index)
-				-- 	state.nextAction = "move"
-				-- end
-			end
-
-
-			if state.id == "search" then
-				if state.activeTime > 2.5 then
-					if not state.turn then
-						robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-						state.turn = true
-					end
-					if state.activeTime > 6.0 then
-						stackPop()
-					end
-				end
-				if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
-					Eyes.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
-				else
-					Eyes.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
-				end
-			end
-
-
-			if state.id == "investigate" then
-				--! disable investigating.
-				-- if not state.nextAction then
-				-- 	local pos = state.pos
-				-- 	robotTurnTowards(state.pos)
-				-- 	headTurnTowards(state.pos)
-				-- 	local nav = stackPush("navigate")
-				-- 	nav.pos = state.pos
-				-- 	nav.timeout = 5.0
-				-- 	state.nextAction = "search"
-				-- elseif state.nextAction == "search" then
-				-- 	stackPush("search")
-				-- 	state.nextAction = "done"
-				-- elseif state.nextAction == "done" then
-				-- 	PlaySound(idleSound, robot.bodyCenter)
-				-- 	stackPop()
-				-- end
-			end
-
-			if state.id == "move" then
-				-- robotTurnTowards(state.pos)
-				-- robot.speed = config.speed
-				-- head.dir = VecCopy(robot.dir)
-				-- local d = VecLength(VecSub(state.pos, robot.transform.pos))
-				-- if d < 2 then
-				-- 	robot.speed = 0
-				-- 	stackPop()
-				-- else
-				-- 	if robot.blocked > 0.5 then
-						-- stackPush("unblock")
-				-- 	end
-				-- end
-			end
-
-			if state.id == "unblock" then
-				-- if not state.dir then
-				-- 	if math.random(0, 10) < 5 then
-				-- 		state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
-				-- 	else
-				-- 		state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
-				-- 	end
-				-- 	state.dir = VecNormalize(state.dir)
-				-- else
-				-- 	robot.dir = state.dir
-				-- 	robot.speed = -math.min(config.speed, 2.0)
-				-- 	if state.activeTime > 1 then
-				-- 		stackPop()
-				-- 	end
-				-- end
-			end
-
-			--Hunt player
-			if state.id == "hunt" then
-				if not state.init then
-					navigationClear()
-					state.init = true
-					state.headAngle = 0
-					state.headAngleTimer = 0
-				end
-				if robot.distToPlayer < 4.0 then
-					robot.dir = VecCopy(robot.dirToPlayer)
-					Eyes.dir = VecCopy(robot.dirToPlayer)
-					robot.speed = 0
-					navigationClear()
-				else
-					navigationSetTarget(Eyes.lastSeenPos, 1.0 + clamp(Eyes.timeSinceLastSeen, 0.0, 4.0))
-					robot.speedScale = config.huntSpeedScale
-					navigationUpdate(dt)
-					if Eyes.canSeePlayer then
-						Eyes.dir = VecCopy(robot.dirToPlayer)
-						state.headAngle = 0
-						state.headAngleTimer = 0
-					else
-						state.headAngleTimer = state.headAngleTimer + dt
-						if state.headAngleTimer > 1.0 then
-							if state.headAngle > 0.0 then
-								state.headAngle = rnd(-1.0, -0.5)
-							elseif state.headAngle < 0 then
-								state.headAngle = rnd(0.5, 1.0)
-							else
-								state.headAngle = rnd(-1.0, 1.0)
-							end
-							state.headAngleTimer = 0
-						end
-						Eyes.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-					end
-				end
-				if navigation.state ~= "move" and Eyes.timeSinceLastSeen < 2 then
-					--Turn towards player if not moving
-					robot.dir = VecCopy(robot.dirToPlayer)
-				end
-				if navigation.state ~= "move" and Eyes.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
-					if VecDist(Eyes.lastSeenPos, robot.bodyCenter) > 3.0 then
-						stackClear()
-						local s = stackPush("investigate")
-						s.pos = VecCopy(Eyes.lastSeenPos)
-					else
-						stackClear()
-						stackPush("huntlost")
-					end
-				end
-			end
-
-			if state.id == "huntlost" then
-				if not state.timer then
-					state.timer = 6
-					state.turnTimer = 1
-				end
-				state.timer = state.timer - dt
-				Eyes.dir = VecCopy(robot.dir)
-				if state.timer < 0 then
-					PlaySound(idleSound, robot.bodyCenter)
-					stackPop()
-				else
-					state.turnTimer = state.turnTimer - dt
-					if state.turnTimer < 0 then
-						robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-						state.turnTimer = rnd(0.5, 1.5)
-					end
-				end
-			end
-
-			--Avoid player
-			if state.id == "avoid" then
-				if not state.init then
-					navigationClear()
-					state.init = true
-					state.headAngle = 0
-					state.headAngleTimer = 0
-				end
-
-				local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform().pos)
-				local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
-				navigationSetTarget(avoidTarget, 1.0)
-				robot.speedScale = config.huntSpeedScale
-				navigationUpdate(dt)
-				if Eyes.canSeePlayer then
-					Eyes.dir = VecNormalize(VecSub(Eyes.lastSeenPos, robot.transform.pos))
-					state.headAngle = 0
-					state.headAngleTimer = 0
-				else
-					state.headAngleTimer = state.headAngleTimer + dt
-					if state.headAngleTimer > 1.0 then
-						if state.headAngle > 0.0 then
-							state.headAngle = rnd(-1.0, -0.5)
-						elseif state.headAngle < 0 then
-							state.headAngle = rnd(0.5, 1.0)
-						else
-							state.headAngle = rnd(-1.0, 1.0)
-						end
-						state.headAngleTimer = 0
-					end
-					Eyes.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-				end
-
-				if navigation.state ~= "move" and Eyes.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
-					stackClear()
-				end
-			end
-
-			--Get up player
-			if state.id == "getup" then
-				if not state.time then
-					state.time = 0
-				end
-				state.time = state.time + dt
-				hover.timeSinceContact = 0
-				if state.time > 1.0 then
-					stackPop()
-				else
-					hoverGetUp()
-				end
-			end
-
-			if state.id == "navigate" then
-				--! disable navigation
-				-- if not state.initialized then
-				-- 	if not state.timeout then state.timeout = 30 end
-				-- 	navigationClear()
-				-- 	navigationSetTarget(state.pos, state.timeout)
-				-- 	state.initialized = true
-				-- else
-				-- 	head.dir = VecCopy(robot.dir)
-				-- 	navigationUpdate(dt)
-				-- 	if navigation.state == "done" or navigation.state == "fail" then
-						stackPop()
-				-- 	end
-				-- end
-			end
-
-			--React to sound
-			if not stackHas("hunt") then
-				if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
-					stackClear()
-					PlaySound(alertSound, robot.bodyCenter)
-					local s = stackPush("investigate")
-					s.pos = hearing.lastSoundPos
-					hearingConsumeSound()
-				end
-			end
-
-			--Seen player
-			if config.huntPlayer and not stackHas("hunt") then
-				if config.canSeePlayer and Eyes.canSeePlayer or robot.canSensePlayer then
-					stackClear()
-					PlaySound(huntSound, robot.bodyCenter)
-					stackPush("hunt")
-				end
-			end
-
-			--Seen player
-			if config.avoidPlayer and not stackHas("avoid") then
-				if config.canSeePlayer and Eyes.canSeePlayer or robot.distToPlayer < 2.0 then
-					stackClear()
-					stackPush("avoid")
-				end
-			end
-
-			--Get up
-			if hover.timeSinceContact > 3.0 and not stackHas("getup") then
-				stackPush("getup")
-			end
-
-			if IsShapeBroken(GetLightShape(Eyes.eye)) then
-				config.hasVision = false
-				config.canSeePlayer = false
-			end
-
-			-- debugState()
-
-			updateCustom(dt)
-		end
-
-		function tick(dt)
-			if not robot.enabled then
-				return
-			end
-
-			if HasTag(robot.body, "turnhostile") then
-				RemoveTag(robot.body, "turnhostile")
-				config.canHearPlayer = true
-				config.canSeePlayer = true
-				config.huntPlayer = true
-				config.aggressive = true
-				config.practice = false
-			end
-
-			--Outline
-			local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform().pos)
-			if dist < config.outline then
-				local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
-				if canBeSeenByPlayer() then
-					a = 0
-				end
-				robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
-				for i=1, #robot.allBodies do
-					DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
-				end
-			end
-
-			--Remove planks and wires after some time
-			local tags = {"plank", "wire"}
-			local removeTimeOut = 10
-			for i=1, #robot.allShapes do
-				local shape = robot.allShapes[i]
-				local joints = GetShapeJoints(shape)
-				for j=1, #joints do
-					local joint = joints[j]
-					for t=1, #tags do
-						local tag = tags[t]
-						if HasTag(joint, tag) then
-							local t = tonumber(GetTagValue(joint, tag)) or 0
-							t = t + dt
-							if t > removeTimeOut then
-								if GetJointType(joint) == "rope" then
-									DetachJointFromShape(joint, shape)
-								else
-									Delete(joint)
-								end
-								break
-							else
-								SetTag(joint, tag, t)
-							end
-						end
-					end
-				end
-			end
-
-			tickCustom(dt)
-
-		end
-
-		function draw()
-			drawCustom()
-		end
-
-	end
-
-	--> Config
-	do
-
-		pType = GetStringParam("type", "")
-		pSpeed = GetFloatParam("speed", 3.5)
-		pTurnSpeed = GetFloatParam("turnspeed", pSpeed)
-
-		config = {}
-		config.hasVision = false
-		config.viewDistance = 25
-		config.viewFov = 150
-		config.canHearPlayer = false
-		config.canSeePlayer = false
-		config.patrol = false
-		config.sensorDist = 5.0
-		config.speed = pSpeed
-		config.turnSpeed = pTurnSpeed
-		config.huntPlayer = false
-		config.huntSpeedScale = 1.6
-		config.avoidPlayer = false
-		config.triggerAlarmWhenSeen = false
-		config.visibilityTimer = 0.3 --Time player must be seen to be identified as enemy (ideal condition)
-		config.lostVisibilityTimer = 5.0 --Time player is seen after losing visibility
-		config.outline = 13
-		config.aimTime = 5.0
-		config.maxSoundDist = 100.0
-		config.aggressive = false
-		config.stepSound = "m"
-		config.practice = false
-
-		PATH_NODE_TOLERANCE = 0.8
-
-		function configInit()
-			local eye = FindLight("eye")
-			local head = FindBody("head")
-			config.patrol = FindLocation("patrol") ~= 0
-			config.hasVision = eye ~= 0
-			config.viewDistance = getTagParameter(eye, "viewdist", config.viewDistance)
-			config.viewFov = getTagParameter(eye, "viewfov", config.viewFov)
-			config.maxSoundDist = getTagParameter(head, "heardist", config.maxSoundDist)
-			if hasWord(pType, "investigate") then
-				config.canHearPlayer = true
-				config.canSeePlayer = true
-			end
-			if hasWord(pType, "chase") then
-				config.canHearPlayer = true
-				config.canSeePlayer = true
-				config.huntPlayer = true
-			end
-			if hasWord(pType, "avoid") and config.patrol then
-				config.avoidPlayer = true
-				config.canSeePlayer = true
-			end
-			if hasWord(pType, "alarm") then
-				config.triggerAlarmWhenSeen = true
-			end
-			if hasWord(pType, "nooutline") then
-				config.outline = 0
-			end
-			if hasWord(pType, "aggressive") then
-				config.aggressive = true
-			end
-			-- if hasWord(pType, "practice") then
-			-- 	config.canSeePlayer = true
-			-- 	config.practice = true
-			-- end
-			local body = FindBody("body")
-			if HasTag(body, "stepsound") then
-				config.stepSound = GetTagValue(body, "stepsound")
-			end
-		end
-
-	end
-
-	--> Navigation
-	do
-
-		navigation = {}
-		navigation.state = "done"
-		navigation.path = {}
-		navigation.target = Vec()
-		navigation.hasNewTarget = false
-		navigation.resultRetrieved = true
-		navigation.deviation = 0		-- Distance to path
-		navigation.blocked = 0
-		navigation.unblockTimer = 0		-- Timer that ticks up when blocked. If reaching limit, unblock kicks in and timer resets
-		navigation.unblock = 0			-- If more than zero, navigation is in unblock mode (reverse direction)
-		navigation.vertical = 0
-		navigation.thinkTime = 0
-		navigation.timeout = 1
-		navigation.lastQueryTime = 0
-		navigation.timeSinceProgress = 0
-
-		function navigationInit()
-			if #wheels.bodies > 0 then
-				navigation.pathType = "low"
-			else
-				navigation.pathType = "standard"
-			end
-		end
-
-		--Prune path backwards so robot don't need to go backwards
-		function navigationPrunePath()
-			if #navigation.path > 0 then
-				for i=#navigation.path, 1, -1 do
-					local p = navigation.path[i]
-					local dv = VecSub(p, robot.transform.pos)
-					local d = VecLength(dv)
-					if d < PATH_NODE_TOLERANCE then
-						--Keep everything after this node and throw out the rest
-						local newPath = {}
-						for j=i, #navigation.path do
-							newPath[#newPath+1] = navigation.path[j]
-						end
-						navigation.path = newPath
-						return
-					end
-				end
-			end
-		end
-
-		function navigationClear()
-			AbortPath()
-			navigation.state = "done"
-			navigation.path = {}
-			navigation.hasNewTarget = false
-			navigation.resultRetrieved = true
-			navigation.deviation = 0
-			navigation.blocked = 0
-			navigation.unblock = 0
-			navigation.vertical = 0
-			navigation.target = Vec(0, -100, 0)
-			navigation.thinkTime = 0
-			navigation.lastQueryTime = 0
-			navigation.unblockTimer = 0
-			navigation.timeSinceProgress = 0
-		end
-
-		function navigationSetTarget(pos, timeout)
-			pos = truncateToGround(pos)
-			if VecDist(navigation.target, pos) > 0 then
-				navigation.target = VecCopy(pos)
-				navigation.hasNewTarget = true
-				navigation.state = "move"
-			end
-			navigation.timeout = timeout
-			navigation.timeSinceProgress = 0
-		end
-
-		function navigationUpdate(dt)
-			if GetPathState() == "busy" then
-				navigation.timeSinceProgress = 0
-				navigation.thinkTime = navigation.thinkTime + dt
-				if navigation.thinkTime > navigation.timeout then
-					AbortPath()
-				end
-			end
-
-			if GetPathState() ~= "busy" then
-				if GetPathState() == "done" or GetPathState() == "fail" then
-					if not navigation.resultRetrieved then
-						if GetPathLength() > 0.5 then
-							for l=0.2, GetPathLength(), 0.2 do
-								navigation.path[#navigation.path+1] = GetPathPoint(l)
-							end
-						end
-						navigation.lastQueryTime = navigation.thinkTime
-						navigation.resultRetrieved = true
-						navigation.state = "move"
-						navigationPrunePath()
-					end
-				end
-				navigation.thinkTime = 0
-			end
-
-			if navigation.thinkTime == 0 and navigation.hasNewTarget then
-				local startPos
-
-				if #navigation.path > 0 and VecDist(navigation.path[1], robot.navigationCenter) < 2.0 then
-					--Keep a little bit of the old path and use last point of that as start position
-					--Use previous query's time as an estimate for the next
-					local distToKeep = VecLength(GetBodyVelocity(robot.body))*navigation.lastQueryTime
-					local nodesToKeep = math.clamp(math.ceil(distToKeep / 0.2), 1, 15)
-					local newPath = {}
-					for i=1, math.min(nodesToKeep, #navigation.path) do
-						newPath[i] = navigation.path[i]
-					end
-					navigation.path = newPath
-					startPos = navigation.path[#navigation.path]
-				else
-					startPos = truncateToGround(robot.transform.pos)
-					navigation.path = {}
-				end
-
-				local targetRadius = 1.0
-				if GetPlayerVehicle()~=0 then
-					targetRadius = 4.0
-				end
-
-				local target = navigation.target
-				-- if robot.limitTrigger ~= 0 then
-				-- 	target = GetTriggerClosestPoint(robot.limitTrigger, target)
-					target = truncateToGround(target)
-				-- end
-
-				QueryRequire("physical large")
-				rejectAllBodies(robot.allBodies)
-				QueryPath(startPos, target, 100, targetRadius, navigation.pathType)
-
-				navigation.timeSinceProgress = 0
-				navigation.hasNewTarget = false
-				navigation.resultRetrieved = false
-				navigation.state = "move"
-			end
-
-			navigationMove(dt)
-
-			if GetPathState() ~= "busy" and #navigation.path == 0 and not navigation.hasNewTarget then
-				if GetPathState() == "done" or GetPathState() == "idle" then
-					navigation.state = "done"
-				else
-					navigation.state = "fail"
-				end
-			end
-		end
-
-		function navigationMove(dt)
-			if #navigation.path > 0 then
-				if navigation.resultRetrieved then
-					--If we have a finished path and didn't progress along it for five seconds, recompute
-					--Should probably only do this for a limited time until giving up
-					navigation.timeSinceProgress = navigation.timeSinceProgress + dt
-					if navigation.timeSinceProgress > 5.0 then
-						navigation.hasNewTarget = true
-						navigation.path = {}
-					end
-				end
-				if navigation.unblock > 0 then
-					robot.speed = -2
-					navigation.unblock = navigation.unblock - dt
-				else
-					local target = navigation.path[1]
-					local dv = VecSub(target, robot.navigationCenter)
-					local distToFirstPathPoint = VecLength(dv)
-					dv[2] = 0
-					local d = VecLength(dv)
-					if distToFirstPathPoint < 2.5 then
-						if d < PATH_NODE_TOLERANCE then
-							if #navigation.path > 1 then
-								--Measure verticality which should decrease speed
-								local diff = VecSub(navigation.path[2], navigation.path[1])
-								navigation.vertical = diff[2] / (VecLength(diff)+0.001)
-								--Remove the first one
-								local newPath = {}
-								for i=2, #navigation.path do
-									newPath[#newPath+1] = navigation.path[i]
-								end
-								navigation.path = newPath
-								navigation.timeSinceProgress = 0
-							else
-								--We're done
-								navigation.path = {}
-								robot.speed = 0
-								return
-							end
-						else
-							--Walk towards first point on path
-							robot.dir = VecCopy(VecNormalize(VecSub(target, robot.transform.pos)))
-
-							local dirDiff = VecDot(VecScale(robot.axes[3], -1), robot.dir)
-							local speedScale = math.max(0.25, dirDiff)
-							speedScale = speedScale * clamp(1.0 - navigation.vertical, 0.3, 1.0)
-							robot.speed = config.speed * speedScale
-
-						end
-					else
-						--Went off path, scrap everything and recompute
-						navigation.hasNewTarget = true
-						navigation.path = {}
-					end
-
-					--Check if stuck
-					-- if robot.blocked > 0.2 then
-					-- 	navigation.blocked = navigation.blocked + dt
-					-- 	if navigation.blocked > 0.2 then
-					-- 		robot.breakAllTimer = 0.1
-					-- 		navigation.blocked = 0.0
-					-- 	end
-					-- 	navigation.unblockTimer = navigation.unblockTimer + dt
-					-- 	if navigation.unblockTimer > 2.0 and navigation.unblock <= 0.0 then
-					-- 		navigation.unblock = 1.0
-					-- 		navigation.unblockTimer = 0
-					-- 	end
-					-- else
-					-- 	navigation.blocked = 0
-					-- 	navigation.unblockTimer = 0
-					-- end
-				end
-			end
-		end
-
-	end
-
-end
-
-
-
---= ROBOT
-do
-	--> Robot
-	do
-
-		robot = {}
-		robot.body = 0
-		robot.transform = Transform()
-		robot.axes = {}
-		robot.bodyCenter = Vec()
-		robot.navigationCenter = Vec()
-		robot.dir = Vec(0, 0, -1)
-		robot.speed = 0
-		robot.blocked = 0
-		robot.mass = 0
-		robot.allBodies = {}
-		robot.allShapes = {}
-		robot.allJoints = {}
-		robot.initialBodyTransforms = {}
-		robot.enabled = true
-		robot.deleted = false
-		robot.speedScale = 1
-		robot.breakAll = false
-		robot.breakAllTimer = 0
-		robot.distToPlayer = 100
-		robot.dirToPlayer = 0
-		robot.roamTrigger = 0
-		robot.limitTrigger = 0
-		robot.investigateTrigger = 0
-		robot.activateTrigger = 0
-		robot.stunned = 0
-		robot.outlineAlpha = 0
-		robot.canSensePlayer = false
-		robot.playerPos = Vec()
-
-
-		function robotSetAxes()
-			robot.transform = GetBodyTransform(robot.body)
-			robot.axes[1] = TransformToParentVec(robot.transform, Vec(1, 0, 0))
-			robot.axes[2] = TransformToParentVec(robot.transform, Vec(0, 1, 0))
-			robot.axes[3] = TransformToParentVec(robot.transform, Vec(0, 0, 1))
-		end
-
-
-		function robotInit()
-			robot.body = FindBody("body")
-			robot.allBodies = FindBodies()
-			robot.allShapes = FindShapes()
-			robot.allJoints = FindJoints()
-			robot.roamTrigger = FindTrigger("roam")
-			robot.limitTrigger = FindTrigger("limit")
-			robot.investigateTrigger = FindTrigger("investigate")
-			robot.activateTrigger = FindTrigger("activate")
-			if robot.activateTrigger ~= 0 then
-				SetTag(robot.body, "inactive")
-			end
-			for i=1, #robot.allBodies do
-				robot.initialBodyTransforms[i] = GetBodyTransform(robot.allBodies[i])
-			end
-			robotSetAxes()
-		end
-
-
-		function robotTurnTowards(pos)
-			robot.dir = VecNormalize(VecSub(pos, robot.transform.pos))
-		end
-
-
-		function robotSetDirAngle(angle)
-			robot.dir[1] = math.cos(angle)
-			robot.dir[3] = math.sin(angle)
-		end
-
-
-		function robotGetDirAngle()
-			return math.atan2(robot.dir[3], robot.dir[1])
-		end
-
-
-		function robotUpdate(dt)
-			robotSetAxes()
-
-			-- if config.practice then
-			-- 	local overrideTarget = FindBody("practicetarget", true)
-			-- 	if overrideTarget ~= 0 then
-			-- 		robot.playerPos = GetBodyTransform(overrideTarget).pos
-			-- 		if not stackHas("navigate") then
-			-- 			robotTurnTowards(robot.playerPos)
-			-- 		end
-			-- 	else
-			-- 		robot.playerPos = Vec(0, -100, 0)
-			-- 	end
-			-- else
-				robot.playerPos = getOuterCrosshairWorldPos()
-			-- end
-
-			-- local vel = GetBodyVelocity(robot.body)
-			-- local fwdSpeed = VecDot(vel, robot.dir)
-			-- local blocked = 0
-			-- if robot.speed > 0 and fwdSpeed > -0.1 then
-			-- 	blocked = 1.0 - clamp(fwdSpeed/0.5, 0.0, 1.0)
-			-- end
-			-- robot.blocked = robot.blocked * 0.95 + blocked * 0.05
-
-			--Always blocked if fall is detected
-			-- if sensor.detectFall > 0 then
-			-- 	robot.blocked = 1.0
-			-- end
-
-			--Evaluate mass every frame since robots can break
-			robot.mass = 0
-			local bodies = FindBodies()
-			for i=1, #bodies do
-				robot.mass = robot.mass + GetBodyMass(bodies[i])
-			end
-
-			robot.bodyCenter = TransformToParentPoint(robot.transform, GetBodyCenterOfMass(robot.body))
-			robot.navigationCenter = TransformToParentPoint(robot.transform, Vec(0, -hover.distTarget, 0))
-
-			--Handle break all
-			robot.breakAllTimer = math.max(0.0, robot.breakAllTimer - dt)
-			if not robot.breakAll and robot.breakAllTimer > 0.0 then
-				for i=1, #robot.allShapes do
-					SetTag(robot.allShapes[i], "breakall")
-				end
-				robot.breakAll = true
-			end
-			if robot.breakAll and robot.breakAllTimer <= 0.0 then
-				for i=1, #robot.allShapes do
-					RemoveTag(robot.allShapes[i], "breakall")
-				end
-				robot.breakAll = false
-			end
-
-			--Distance and direction to player
-			local pp = VecAdd(GetPlayerTransform().pos, Vec(0, 1, 0))
-			local d = VecSub(pp, robot.bodyCenter)
-			robot.distToPlayer = VecLength(d)
-			robot.dirToPlayer = VecScale(d, 1.0/robot.distToPlayer)
-
-
-			--Sense player if player is close and there is nothing in between
-			robot.canSensePlayer = false
-			if robot.distToPlayer < 3.0 then
-				rejectAllBodies(robot.allBodies)
-				if not QueryRaycast(robot.bodyCenter, robot.dirToPlayer, robot.distToPlayer) then
-					robot.canSensePlayer = true
-				end
-			end
-
-			--Robot body sounds
-			if robot.enabled and hover.contact > 0 then
-				local vol
-				vol = clamp(VecLength(GetBodyVelocity(robot.body)) * 0.4, 0.0, 1.0)
-				if vol > 0 then
-					PlayLoop(walkLoop, robot.transform.pos, vol)
-				end
-
-				vol = clamp(VecLength(GetBodyAngularVelocity(robot.body)) * 0.4, 0.0, 1.0)
-				if vol > 0 then
-					PlayLoop(turnLoop, robot.transform.pos, vol)
-				end
-			end
-		end
-
-	end
-
-	--> Head
-	do
-
-		Eyes = {}
-		Eyes.body = 0
-		Eyes.eye = 0
-		Eyes.dir = Vec(0,0,-1)
-		Eyes.lookOffset = 0
-		Eyes.lookOffsetTimer = 0
-		Eyes.canSeePlayer = false
-		Eyes.lastSeenPos = Vec(0,0,0)
-		Eyes.timeSinceLastSeen = 999
-		Eyes.seenTimer = 0
-		Eyes.alarmTimer = 0
-		Eyes.alarmTime = 2.0
-		Eyes.aim = 0	-- 1.0 = perfect aim, 0.0 = will always miss player. This increases when robot sees player based on config.aimTime
-
-		function headInit()
-			Eyes.body = FindBody("head")
-			Eyes.eye = FindLight("eye")
-			Eyes.joint = FindJoint("head")
-			Eyes.alarmTime = getTagParameter(Eyes.eye, "alarm", 2.0)
-		end
-
-		function headTurnTowards(pos)
-			Eyes.dir = VecNormalize(VecSub(pos, GetBodyTransform(Eyes.body).pos))
-		end
-
-		function headUpdate(dt)
-			local t = GetBodyTransform(Eyes.body)
-			local fwd = TransformToParentVec(t, Vec(0, 0, -1))
-
-			--Check if head can see player
-			local et = GetLightTransform(Eyes.eye)
-			local pp = VecCopy(robot.playerPos)
-			local toPlayer = VecSub(pp, et.pos)
-			local distToPlayer = VecLength(toPlayer)
-			toPlayer = VecNormalize(toPlayer)
-
-			--Determine player visibility
-			local playerVisible = false
-			if config.hasVision and config.canSeePlayer then
-				if distToPlayer < config.viewDistance then	--Within view distance
-					local limit = math.cos(config.viewFov * 0.5 * math.pi / 180)
-					if VecDot(toPlayer, fwd) > limit then --In view frustum
-						rejectAllBodies(robot.allBodies)
-						QueryRejectVehicle(GetPlayerVehicle())
-						if not QueryRaycast(et.pos, toPlayer, distToPlayer, 0, true) then --Not blocked
-							playerVisible = true
-						end
-					end
-				end
-			end
-
-			if config.aggressive then
-				playerVisible = true
-			end
-
-			--If player is visible it takes some time before registered as seen
-			--If player goes out of sight, head can still see for some time second (approximation of motion estimation)
-			if playerVisible then
-				local distanceScale = clamp(1.0 - distToPlayer/config.viewDistance, 0.5, 1.0)
-				local angleScale = clamp(VecDot(toPlayer, fwd), 0.5, 1.0)
-				local delta = (dt * distanceScale * angleScale) / (config.visibilityTimer / 0.5)
-				Eyes.seenTimer = math.min(1.0, Eyes.seenTimer + delta)
-			else
-				Eyes.seenTimer = math.max(0.0, Eyes.seenTimer - dt / config.lostVisibilityTimer)
-			end
-			Eyes.canSeePlayer = (Eyes.seenTimer > 0.5)
-
-			if Eyes.canSeePlayer then
-				Eyes.lastSeenPos = pp
-				Eyes.timeSinceLastSeen = 0
-			else
-				Eyes.timeSinceLastSeen = Eyes.timeSinceLastSeen + dt
-			end
-
-			if playerVisible and Eyes.canSeePlayer then
-				Eyes.aim = math.min(1.0, Eyes.aim + dt / config.aimTime)
-			else
-				Eyes.aim = math.max(0.0, Eyes.aim - dt / config.aimTime)
-			end
-
-			if config.triggerAlarmWhenSeen then
-				local red = false
-				if GetBool("level.alarm") then
-					red = math.mod(GetTime(), 0.5) > 0.25
-				else
-					if playerVisible and IsPointAffectedByLight(Eyes.eye, pp) then
-						red = true
-						Eyes.alarmTimer = Eyes.alarmTimer + dt
-						PlayLoop(chargeLoop, robot.transform.pos)
-						if Eyes.alarmTimer > Eyes.alarmTime and playerVisible then
-							SetBool("level.alarm", true)
-						end
-					else
-						Eyes.alarmTimer = math.max(0.0, Eyes.alarmTimer - dt)
-					end
-				end
-				if red then
-					SetLightColor(Eyes.eye, 1, 0, 0)
-				else
-					SetLightColor(Eyes.eye, 1, 1, 1)
-				end
-			end
-
-			--Rotate head to head.dir
-			local fwd = TransformToParentVec(t, Vec(0, 0, -1))
-			if playerVisible then
-				headTurnTowards(pp)
-			end
-			Eyes.dir = VecNormalize(Eyes.dir)
-			--end
-			local c = VecCross(fwd, Eyes.dir)
-			local d = VecDot(c, robot.axes[2])
-			local angVel = clamp(d*10, -3, 3)
-			local f = 100
-			mi, ma = GetJointLimits(Eyes.joint)
-			local ang = GetJointMovement(Eyes.joint)
-			if ang < mi+1 and angVel < 0 then
-				angVel = 0
-			end
-			if ang > ma-1 and angVel > 0 then
-				angVel = 0
-			end
-
-			ConstrainAngularVelocity(Eyes.body, robot.body, robot.axes[2], angVel, -f , f)
-
-			local vol = clamp(math.abs(angVel)*0.3, 0.0, 1.0)
-			if vol > 0 then
-				PlayLoop(headLoop, robot.transform.pos, vol)
-			end
-		end
-
-	end
-
-	--> Feet
-	do
-		feet = {}
-
-		function feetInit()
-			local f = FindBodies("foot")
-			for i=1, #f do
-				local foot = {}
-				foot.body = f[i]
-				local t = GetBodyTransform(foot.body)
-				local rayOrigin = TransformToParentPoint(t, Vec(0, 0.9, 0))
-				local rayDir = TransformToParentVec(t, Vec(0, -1, 0))
-
-				foot.lastTransform = TransformCopy(t)
-				foot.targetTransform = TransformCopy(t)
-				foot.candidateTransform = TransformCopy(t)
-				foot.worldTransform = TransformCopy(t)
-				foot.stepAge = 1
-				foot.stepLifeTime = 1
-				foot.localRestTransform = TransformToLocalTransform(robot.transform, t)
-				foot.localTransform = TransformCopy(foot.localRestTransform)
-				foot.rayOrigin = TransformToLocalPoint(robot.transform, rayOrigin)
-				foot.rayDir = TransformToLocalVec(robot.transform, rayDir)
-				foot.rayDist = hover.distTarget + hover.distPadding
-				foot.contact = true
-				local mass = GetBodyMass(foot.body)
-				foot.linForce = 20 * mass
-				foot.angForce = 1 * mass
-				local linScale, angScale = getTagParameter2(foot.body, "force", 1.0)
-				foot.linForce = foot.linForce * linScale
-				foot.angForce = foot.angForce * angScale
-				feet[i] = foot
-			end
-		end
-
-
-		function feetCollideLegs(enabled)
-			local mask = 0
-			if enabled then
-				mask = 253
-			end
-			local feet = FindBodies("foot")
-			for i=1, #feet do
-				local shapes = GetBodyShapes(feet[i])
-				for j=1, #shapes do
-					SetShapeCollisionFilter(shapes[j], 2, mask)
-				end
-			end
-			local legs = FindBodies("leg")
-			for i=1, #legs do
-				local shapes = GetBodyShapes(legs[i])
-				for j=1, #shapes do
-					SetShapeCollisionFilter(shapes[j], 2, mask)
-				end
-			end
-			for i=1, #wheels.bodies do
-				local shapes = GetBodyShapes(wheels.bodies[i])
-				for j=1, #shapes do
-					SetShapeCollisionFilter(shapes[j], 2, mask)
-				end
-			end
-		end
-
-
-		function feetUpdate(dt)
-			if robot.stunned > 0 then
-				feetCollideLegs(true)
-				return
-			else
-				feetCollideLegs(false)
-			end
-
-			local vel = GetBodyVelocity(robot.body)
-			local velLength = VecLength(vel)
-			local stepLength = clamp(velLength*1.5, 0.5, 1)
-			local stepTime = math.min(stepLength / velLength * 0.5, 0.25)
-			local stepHeight = stepLength * 0.5
-
-			local inStep = false
-			for i=1, #feet do
-
-				local q = feet[i].stepAge/feet[i].stepLifeTime
-				if feet[i].stepLifeTime > stepTime then
-					feet[i].stepLifeTime = stepTime
-				end
-				if q < 0.8 then
-					inStep = true
-				end
-			end
-
-			for i=1, #feet do
-				local foot = feet[i]
-
-				if not inStep then
-					--Find candidate footstep
-					local tPredict = TransformCopy(robot.transform)
-					tPredict.pos = VecAdd(tPredict.pos, VecScale(VecLerp(VecScale(robot.dir, robot.speed), vel, 0.5), stepTime*1.5))
-					local rayOrigin = TransformToParentPoint(tPredict, foot.rayOrigin)
-					local rayDir = TransformToParentVec(tPredict, foot.rayDir)
-					QueryRequire("physical large")
-					rejectAllBodies(robot.allBodies)
-					local hit, dist, normal, shape = QueryRaycast(rayOrigin, rayDir, foot.rayDist)
-					local targetTransform = TransformToParentTransform(robot.transform, foot.localRestTransform)
-					if hit then
-						targetTransform.pos = VecAdd(rayOrigin, VecScale(rayDir, dist))
-					end
-					foot.candidateTransform = targetTransform
-				end
-
-				--Animate foot
-				if hover.contact > 0 then
-					if foot.stepAge < foot.stepLifeTime then
-						foot.stepAge = math.min(foot.stepAge + dt, foot.stepLifeTime)
-						local q = foot.stepAge / foot.stepLifeTime
-						q = q * q * (3.0 - 2.0 * q) -- smoothstep
-						local p = VecLerp(foot.lastTransform.pos, foot.targetTransform.pos, q)
-						p[2] = p[2] + math.sin(math.pi * q)*stepHeight
-						local r = QuatSlerp(foot.lastTransform.rot, foot.targetTransform.rot, q)
-						foot.worldTransform = Transform(p, r)
-						foot.localTransform = TransformToLocalTransform(robot.transform, foot.worldTransform)
-						if foot.stepAge == foot.stepLifeTime then
-							PlaySound(stepSound, p, 0.5)
-						end
-					end
-					ConstrainPosition(foot.body, robot.body, GetBodyTransform(foot.body).pos, foot.worldTransform.pos, 8, foot.linForce)
-					ConstrainOrientation(foot.body, robot.body, GetBodyTransform(foot.body).rot, foot.worldTransform.rot, 16, foot.angForce)
-				end
-
-			end
-
-			if not inStep then
-				--Find best step candidate
-				local bestFoot = 0
-				local bestDist = 0
-				for i=1, #feet do
-					local foot = feet[i]
-					local dist = VecLength(VecSub(foot.targetTransform.pos, foot.candidateTransform.pos))
-					if dist > stepLength and dist > bestDist then
-						bestDist = dist
-						bestFoot = i
-					end
-				end
-				--Initiate best footstep
-				if bestFoot ~= 0 then
-					local foot = feet[bestFoot]
-					foot.lastTransform = TransformCopy(GetBodyTransform(foot.body))
-					foot.targetTransform = TransformCopy(foot.candidateTransform)
-					foot.stepAge = 0
-					foot.stepLifeTime = stepTime
-				end
-			end
-		end
-	end
-
-	--> Hover
-	do
-
-		hover = {}
-		hover.hitBody = 0
-		hover.contact = 0.0
-		hover.distTarget = 0.3
-		hover.distPadding = 0.3
-		hover.timeSinceContact = 0.0
-
-
-		function hoverInit()
-			local bodyPos = robot.transform.pos
-			local footMin, footMax = GetBodyBounds(FindBodies('foot')[1])
-			local dist = bodyPos[2] - footMin[2]
-
-			-- local maxDist = 2.0
-			-- local hit, dist = QueryRaycast(robot.transform.pos, VecScale(robot.axes[2], -1), maxDist)
-			-- if hit then
-				hover.distTarget = dist
-				hover.distPadding = math.min(0.3, dist*0.5)
-			-- end
-		end
-
-
-		function hoverFloat()
-			if hover.contact > 0 then
-				local d = clamp(hover.distTarget - hover.currentDist, -0.2, 0.2)
-				local v = d * 10
-				local f = hover.contact * math.max(0, d*robot.mass*5.0) + robot.mass*0.2
-				ConstrainVelocity(robot.body, hover.hitBody, robot.bodyCenter, Vec(0,1,0), v, 0 , f)
-			end
-		end
-
-
-		UPRIGHT_STRENGTH = 1.0	-- Spring strength
-		UPRIGHT_MAX = 0.5		-- Max spring force
-		UPRIGHT_BASE = 0.1		-- Fraction of max spring force to always apply (less springy)
-		function hoverUpright()
-			local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
-			axes = {}
-			axes[1] = Vec(1,0,0)
-			axes[2] = Vec(0,1,0)
-			axes[3] = Vec(0,0,1)
-			for a = 1, 3, 2 do
-				local d = VecDot(up, axes[a])
-				local v = math.clamp(d * 15, -2, 2)
-				local f = math.clamp(math.abs(d)*UPRIGHT_STRENGTH, -UPRIGHT_MAX, UPRIGHT_MAX)
-				f = f + UPRIGHT_MAX * UPRIGHT_BASE
-				f = f * robot.mass
-				f = f * hover.contact
-				--f = 10000
-				ConstrainAngularVelocity(robot.body, hover.hitBody, axes[a], v, -f , f)
-			end
-		end
-
-
-		function hoverGetUp()
-			local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
-			axes = {}
-			axes[1] = Vec(1,0,0)
-			axes[2] = Vec(0,1,0)
-			axes[3] = Vec(0,0,1)
-			for a = 1, 3, 2 do
-				local d = VecDot(up, axes[a])
-				local v = math.clamp(d * 15, -2, 2)
-				local f = math.clamp(math.abs(d)*UPRIGHT_STRENGTH, -UPRIGHT_MAX, UPRIGHT_MAX)
-				f = f + UPRIGHT_MAX * UPRIGHT_BASE
-				f = f * robot.mass
-				ConstrainAngularVelocity(robot.body, hover.hitBody, axes[a], v, -f , f)
-			end
-		end
-
-
-		function hoverTurn()
-			local fwd = VecScale(robot.axes[3], -1)
-			local c = VecCross(fwd, robot.dir)
-			local d = VecDot(c, robot.axes[2])
-			local angVel = clamp(d*10, -config.turnSpeed * robot.speedScale, config.turnSpeed * robot.speedScale)
-
-			local curr = VecDot(robot.axes[2], GetBodyAngularVelocity(robot.body))
-			angVel = curr + clamp(angVel - curr, -0.2*robot.speedScale, 0.2*robot.speedScale)
-
-			-- local f = robot.mass*0.5 * hover.contact
-			local f = robot.mass*0.5 * hover.contact
-			ConstrainAngularVelocity(robot.body, hover.hitBody, robot.axes[2], angVel, -f , f)
-		end
-
-
-		function hoverMove()
-			local desiredSpeed = robot.speed * robot.speedScale
-			local fwd = VecScale(robot.axes[3], -1)
-			fwd[2] = 0
-			fwd = VecNormalize(fwd)
-			local side = VecCross(Vec(0,1,0), fwd)
-			local currSpeed = VecDot(fwd, GetBodyVelocityAtPos(robot.body, robot.bodyCenter))
-			local speed = currSpeed + clamp(desiredSpeed - currSpeed/2, -0.05*robot.speedScale, 0.05*robot.speedScale)
-			local f = robot.mass*0.2 * hover.contact
-
-			ConstrainVelocity(robot.body, hover.hitBody, robot.bodyCenter, fwd, speed, -f , f)
-			ConstrainVelocity(robot.body, hover.hitBody, robot.bodyCenter, robot.axes[1], 0, -f , f)
-		end
-
-
-		BALANCE_RADIUS = 0.4
-		function hoverUpdate(dt)
-			local dir = VecScale(robot.axes[2], -1)
-
-			--Shoot rays from four locations downwards
-			local hit = false
-			local dist = 0
-			local normal = Vec(0,0,0)
-			local shape = 0
-			local samples = {}
-			samples[#samples+1] = Vec(-BALANCE_RADIUS,0,0)
-			samples[#samples+1] = Vec(BALANCE_RADIUS,0,0)
-			samples[#samples+1] = Vec(0,0,BALANCE_RADIUS)
-			samples[#samples+1] = Vec(0,0,-BALANCE_RADIUS)
-			local castRadius = 0.1
-			local maxDist = hover.distTarget + hover.distPadding
-			for i=1, #samples do
-				QueryRequire("physical large")
-				rejectAllBodies(robot.allBodies)
-				local origin = TransformToParentPoint(robot.transform, samples[i])
-				local rhit, rdist, rnormal, rshape = QueryRaycast(origin, dir, maxDist, castRadius)
-				if rhit then
-					hit = true
-					dist = dist + rdist + castRadius
-					if rdist == 0 then
-						--Raycast origin in geometry, normal unsafe. Assume upright
-						rnormal = Vec(0,1,0)
-					end
-					if shape == 0 then
-						shape = rshape
-					else
-						local b = GetShapeBody(rshape)
-						local bb = GetShapeBody(shape)
-						--Prefer new hit if it's static or has more mass than old one
-						if not IsBodyDynamic(b) or (IsBodyDynamic(bb) and GetBodyMass(b) > GetBodyMass(bb)) then
-							shape = rshape
-						end
-					end
-					normal = VecAdd(normal, rnormal)
-				else
-					dist = dist + maxDist
-				end
-			end
-
-			--Use average of rays to determine contact and height
-			if hit then
-				dist = dist / #samples
-				normal = VecNormalize(normal)
-				hover.hitBody = GetShapeBody(shape)
-				if IsBodyDynamic(hover.hitBody) and GetBodyMass(hover.hitBody) < 300 then
-					--Hack alert! Treat small bodies as static to avoid sliding and glitching around on debris
-					hover.hitBody = 0
-				end
-				hover.currentDist = dist
-				hover.contact = clamp(1.0 - (dist - hover.distTarget) / hover.distPadding, 0.0, 1.0)
-				hover.contact = hover.contact * math.max(0, normal[2])
-			else
-				hover.hitBody = 0
-				hover.currentDist = maxDist
-				hover.contact = 0
-			end
-
-			--Limit body angular velocity magnitude to 10 rad/s at max contact
-			if hover.contact > 0 then
-				local maxAngVel = 10.0 / hover.contact
-				local angVel = GetBodyAngularVelocity(robot.body)
-				local angVelLength = VecLength(angVel)
-				if angVelLength > maxAngVel then
-					SetBodyAngularVelocity(robot.body, VecScale(maxAngVel / angVelLength))
-				end
-			end
-
-			if hover.contact > 0 then
-				hover.timeSinceContact = 0
-			else
-				hover.timeSinceContact = hover.timeSinceContact + dt
-			end
-
-			hoverFloat()
-			hoverUpright()
-			hoverTurn()
-			hoverMove()
-		end
-
-	end
-
-	--> Wheels
-	do
-
-		wheels = {}
-		wheels.bodies = {}
-		wheels.transforms = {}
-		wheels.radius = {}
-
-		function wheelsInit()
-			wheels.bodies = FindBodies("wheel")
-			for i=1, #wheels.bodies do
-				local t = GetBodyTransform(wheels.bodies[i])
-				local shape = GetBodyShapes(wheels.bodies[i])[1]
-				local sx, sy, sz = GetShapeSize(shape)
-				wheels.transforms[i] = TransformToLocalTransform(robot.transform, t)
-				wheels.radius[i] = math.max(sx, sz)*0.05
-			end
-		end
-
-		function wheelsUpdate(dt)
-			for i=1, #wheels.bodies do
-				local v = GetBodyVelocityAtPos(robot.body, TransformToParentPoint(robot.transform, wheels.transforms[i].pos))
-				local lv = VecDot(robot.axes[3], v)
-				if hover.contact > 0 then
-					local shapes = GetBodyShapes(wheels.bodies[i])
-					if #shapes > 0 then
-						local joints = GetShapeJoints(shapes[1])
-						if #joints > 0 then
-							local angVel = lv / wheels.radius[i]
-							SetJointMotor(joints[1], angVel, 100)
-						end
-					end
-					PlayLoop(rollLoop, robot.transform.pos, clamp(math.abs(lv)*0.5, 0.0, 1.0))
-				end
-			end
-		end
-
-	end
-
-	--> Weapons
-	do
-
-		weapons = {}
-
-		function weaponsInit()
-			local locs = FindLocations("weapon")
-			for i=1, #locs do
-				local loc = locs[i]
-				local t = GetLocationTransform(loc)
-				QueryRequire("dynamic large")
-				local hit, point, normal, shape = QueryClosestPoint(t.pos, 0.15)
-				if hit then
-					local weapon = {}
-					weapon.type = GetTagValue(loc, "weapon")
-					weapon.timeBetweenRounds = tonumber(GetTagValue(loc, "idle"))
-					weapon.chargeTime = tonumber(GetTagValue(loc, "charge"))
-					weapon.fireCooldown = tonumber(GetTagValue(loc, "cooldown"))
-					weapon.shotsPerRound = tonumber(GetTagValue(loc, "count"))
-					weapon.spread = tonumber(GetTagValue(loc, "spread"))
-					weapon.strength = tonumber(GetTagValue(loc, "strength"))
-					weapon.maxDist = tonumber(GetTagValue(loc, "maxdist"))
-					if weapon.type == "" then weapon.type = "gun" end
-					if not weapon.timeBetweenRounds then weapon.timeBetweenRounds = 1 end
-					if not weapon.chargeTime then weapon.chargeTime = 1.2 end
-					if not weapon.fireCooldown then weapon.fireCooldown = 0.15 end
-					if not weapon.shotsPerRound then weapon.shotsPerRound = 8 end
-					if not weapon.spread then weapon.spread = 0.01 end
-					if not weapon.strength then weapon.strength = 1.0 end
-					if not weapon.maxDist then weapon.maxDist = 100.0 end
-					local b = GetShapeBody(shape)
-					local bt = GetBodyTransform(b)
-					weapon.localTransform = TransformToLocalTransform(bt, t)
-					weapon.body = b
-					weapon.state = "idle"
-					weapon.idleTimer = 0
-					weapon.chargeTimer = 0
-					weapon.fireTimer = 0
-					weapon.fireCount = 0
-					weapons[i] = weapon
-				end
-			end
-		end
-
-		function getPerpendicular(dir)
-			local perp = VecNormalize(Vec(rnd(-1, 1), rnd(-1, 1), rnd(-1, 1)))
-			perp = VecNormalize(VecSub(perp, VecScale(dir, VecDot(dir, perp))))
-			return perp
-		end
-
-		function weaponFire(weapon, pos, dir)
-			local perp = getPerpendicular(dir)
-
-			-- This is the default bullet spread
-			local spread =  1 * rnd(0.0, 1.0)
-
-			-- Add more spread up based on aim, so that the first bullets never (well, rarely) hit player
-			local extraSpread = math.min(0.5, 2.0 / robot.distToPlayer)
-			spread = spread	+ (1.0-Eyes.aim) * extraSpread
-
-			dir = VecNormalize(VecAdd(dir, VecScale(perp, spread)))
-
-			--Start one voxel ahead to not hit robot itself
-			pos = VecAdd(pos, VecScale(dir, 0.1))
-
-			if weapon.type == "gun" then
-				PlaySound(shootSound, pos)
-				PointLight(pos, 1, 0.8, 0.6, 5)
-				Shoot(pos, dir, 0, weapon.strength)
-			elseif weapon.type == "rocket" then
-				PlaySound(rocketSound, pos)
-				Shoot(pos, dir, 1, weapon.strength)
-			end
-		end
-
-		function weaponsReset()
-			for i=1, #weapons do
-				weapons[i].state = "idle"
-				weapons[i].idleTimer = weapons[i].timeBetweenRounds
-				weapons[i].fire = 0
-			end
-		end
-
-		function weaponEmitFire(weapon, t, amount)
-			local p = TransformToParentPoint(t, Vec(0, 0, -0.1))
-			local d = TransformToParentVec(t, Vec(0, 0, -1))
-			ParticleReset()
-			ParticleTile(5)
-			ParticleColor(1, 1, 0.5, 1, 0, 0)
-			ParticleRadius(0.1*amount, 1*amount)
-			ParticleEmissive(10, 0)
-			ParticleDrag(0.1)
-			ParticleGravity(math.random()*20)
-			PointLight(p, 1, 0.8, 0.2, 2*amount)
-			PlayLoop(fireLoop, t.pos, amount)
-			SpawnParticle(p, VecScale(d, 12), 0.5 * amount)
-
-			if amount > 0.5 then
-				--Spawn fire
-				if not spawnFireTimer then
-					spawnFireTimer = 0
-				end
-				if spawnFireTimer > 0 then
-					spawnFireTimer = math.max(spawnFireTimer-0.01667, 0)
-				else
-					rejectAllBodies(robot.allBodies)
-					local hit, dist = QueryRaycast(p, d, 3)
-					if hit then
-						local wp = VecAdd(p, VecScale(d, dist))
-						SpawnFire(wp)
-						spawnFireTimer = 1
-					end
-				end
-
-				--Hurt player
-				local toPlayer = VecSub(GetPlayerCameraTransform().pos, t.pos)
-				local distToPlayer = VecLength(toPlayer)
-				local distScale = clamp(1.0 - distToPlayer / 5.0, 0.0, 1.0)
-				if distScale > 0 then
-					toPlayer = VecNormalize(toPlayer)
-					if VecDot(d, toPlayer) > 0.8 or distToPlayer < 0.5 then
-						rejectAllBodies(robot.allBodies)
-						local hit = QueryRaycast(p, toPlayer, distToPlayer)
-						if not hit or distToPlayer < 0.5 then
-							SetPlayerHealth(GetPlayerHealth() - 0.015 * weapon.strength * amount * distScale)
-						end
-					end
-				end
-			end
-		end
-
-		function weaponsUpdate(dt)
-			for i=1, #weapons do
-				local weapon = weapons[i]
-				local bt = GetBodyTransform(weapon.body)
-				local t = TransformToParentTransform(bt, weapon.localTransform)
-				local fwd = TransformToParentVec(t, Vec(0, 0, -1))
-				t.pos = VecAdd(t.pos, VecScale(fwd, 0.15))
-				local playerPos = VecCopy(robot.playerPos)
-				local toPlayer = VecSub(playerPos, t.pos)
-				local distToPlayer = VecLength(toPlayer)
-				toPlayer = VecNormalize(toPlayer)
-				local clearShot = false
-
-				if weapon.type == "fire" then
-					if not weapon.fire then
-						weapon.fire = 0
-					end
-					if Eyes.canSeePlayer and robot.distToPlayer < 8.0 then
-						weapon.fire = math.min(weapon.fire + 0.1, 1.0)
-					else
-						weapon.fire = math.max(weapon.fire - dt*0.5, 0.0)
-					end
-					if weapon.fire > 0 then
-						weaponEmitFire(weapon, t, weapon.fire)
-					else
-						weaponEmitFire(weapon, t, math.max(weapon.fire, 0.1))
-					end
-				else
-					--Need to point towards player and have clear line of sight to have clear shot
-					local towardsPlayer = VecDot(fwd, toPlayer)
-					local gotAim = towardsPlayer > 0.9
-					if distToPlayer < 1.0 and towardsPlayer > 0.0 then
-						gotAim = true
-					end
-					if Eyes.canSeePlayer and gotAim and robot.distToPlayer < weapon.maxDist then
-						QueryRequire("physical large")
-						rejectAllBodies(robot.allBodies)
-						local hit = QueryRaycast(t.pos, fwd, distToPlayer, 0, true)
-						if not hit then
-							clearShot =  true
-						end
-					end
-
-					--Handle states
-					if weapon.state == "idle" then
-						weapon.idleTimer = weapon.idleTimer - dt
-						if weapon.idleTimer <= 0 and clearShot then
-							weapon.state = "charge"
-							weapon.fireDir = fwd
-							weapon.chargeTimer = weapon.chargeTime
-						end
-					elseif weapon.state == "charge" or weapon.state == "chargesilent" then
-						weapon.chargeTimer = weapon.chargeTimer - dt
-						if weapon.state ~= "chargesilent" then
-							PlayLoop(chargeLoop, t.pos)
-						end
-						if weapon.chargeTimer <= 0 then
-							weapon.state = "fire"
-							weapon.fireTimer = 0
-							weapon.fireCount = weapon.shotsPerRound
-						end
-					elseif weapon.state == "fire" then
-						weapon.fireTimer = weapon.fireTimer - dt
-						if towardsPlayer > 0.3 or distToPlayer < 1.0 then
-							if weapon.fireTimer <= 0 then
-								weaponFire(weapon, t.pos, fwd)
-								weapon.fireCount = weapon.fireCount - 1
-								if weapon.fireCount <= 0 then
-									if clearShot then
-										weapon.state = "chargesilent"
-										weapon.chargeTimer = weapon.chargeTime
-									else
-										weapon.state = "idle"
-										weapon.idleTimer = weapon.timeBetweenRounds
-									end
-								else
-									weapon.fireTimer = weapon.fireCooldown
-								end
-							end
-						else
-							--We are no longer pointing towards player, abort round
-							weapon.state = "idle"
-							weapon.idleTimer = weapon.timeBetweenRounds
-						end
-					end
-				end
-			end
-		end
-
-	end
-
-	--> Aims
-	do
-
-		aims = {}
-		aims_lights = {}
-
-		function aimsInit()
-			--! Added aims_lights
-			local lights = FindLights('weap_secondary')
-			local bodies = FindBodies("aim")
-			for i=1, #bodies do
-				local aim = {}
-				aim.body = bodies[i]
-				aims[i] = aim
-
-				for key, light in pairs(lights) do
-					local body = GetLightShape(light)
-					if body == aim.body then
-						aims_lights[i] = light
-					end
-				end
-
-			end
-		end
-
-		function aimsUpdate(dt)
-			for i=1, #aims do
-
-				local aim = aims[i]
-				local playerPos = getOuterCrosshairWorldPos()
-				local toPlayer = VecNormalize(VecSub(playerPos, GetBodyTransform(aim.body).pos))
-				local fwd = TransformToParentVec(GetBodyTransform(robot.body), Vec(0, 0, -1))
-
-				if (Eyes.canSeePlayer and VecDot(fwd, toPlayer) > 0.5) or robot.distToPlayer < 4.0 then
-					--Should aim
-					local v = 2
-					local f = 20
-					local wt = GetBodyTransform(aim.body)
-					local toPlayerOrientation = QuatLookAt(wt.pos, playerPos)
-					ConstrainOrientation(aim.body, robot.body, wt.rot, toPlayerOrientation, v, f)
-				else
-					--Should not aim
-					local rd = TransformToParentVec(GetBodyTransform(robot.body), Vec(0, 0, -1))
-					local wd = TransformToParentVec(GetBodyTransform(aim.body), Vec(0, 0, -1))
-					local angle = clamp(math.acos(VecDot(rd, wd)), 0, 1)
-					local v = 2
-					local f = math.abs(angle) * 10 + 3
-					ConstrainOrientation(robot.body, aim.body, GetBodyTransform(robot.body).rot, GetBodyTransform(aim.body).rot, v, f)
-				end
-
-			end
-		end
-
-	end
-
-	--> Sensor
-	do
-		sensor = {}
-		sensor.blocked = 0
-		sensor.blockedLeft = 0
-		sensor.blockedRight = 0
-		sensor.detectFall = 0
-
-		function sensorInit()
-		end
-
-		function sensorGetBlocked(dir, maxDist)
-			dir = VecNormalize(VecAdd(dir, rndVec(0.3)))
-			local origin = TransformToParentPoint(robot.transform, Vec(0, 0.8, 0))
-			QueryRequire("physical large")
-			rejectAllBodies(robot.allBodies)
-			local hit, dist = QueryRaycast(origin, dir, maxDist)
-			return 1.0 - dist/maxDist
-		end
-
-		function sensorDetectFall()
-			dir = Vec(0, -1, 0)
-			local lookAheadDist = 0.6 + clamp(VecLength(GetBodyVelocity(robot.body))/6.0, 0.0, 0.6)
-			local origin = TransformToParentPoint(robot.transform, Vec(0, 0.5, -lookAheadDist))
-			QueryRequire("physical large")
-			rejectAllBodies(robot.allBodies)
-			local maxDist = hover.distTarget + 1.0
-			local hit, dist = QueryRaycast(origin, dir, maxDist, 0.2)
-			return not hit
-		end
-
-		function sensorUpdate(dt)
-			local maxDist = config.sensorDist
-			local blocked = sensorGetBlocked(TransformToParentVec(robot.transform, Vec(0, 0, -1)), maxDist)
-			if sensorDetectFall() then
-				sensor.detectFall = 1.0
-			else
-				sensor.detectFall = 0.0
-			end
-			sensor.blocked = sensor.blocked * 0.9 + blocked * 0.1
-
-			local blockedLeft = sensorGetBlocked(TransformToParentVec(robot.transform, Vec(-0.5, 0, -1)), maxDist)
-			sensor.blockedLeft = sensor.blockedLeft * 0.9 + blockedLeft * 0.1
-
-			local blockedRight = sensorGetBlocked(TransformToParentVec(robot.transform, Vec(0.5, 0, -1)), maxDist)
-			sensor.blockedRight = sensor.blockedRight * 0.9 + blockedRight * 0.1
-		end
-
-	end
-
-	--> Hearing
-	do
-
-		hearing = {}
-		hearing.lastSoundPos = Vec(0, -100, 0)
-		hearing.lastSoundVolume = 0
-		hearing.timeSinceLastSound = 0
-		hearing.hasNewSound = false
-
-		function hearingInit()
-		end
-
-		function hearingUpdate(dt)
-			hearing.timeSinceLastSound = hearing.timeSinceLastSound + dt
-			if config.canHearPlayer then
-				local vol, pos = GetLastSound()
-				local dist = VecDist(robot.transform.pos, pos)
-				if vol > 0.1 and dist > 4.0 and dist < config.maxSoundDist then
-					local valid = true
-					--If there is an investigation trigger, the robot is in it and the sound is not, ignore sound
-					if robot.investigateTrigger ~= 0 and IsPointInTrigger(robot.investigateTrigger, robot.bodyCenter) and not IsPointInTrigger(robot.investigateTrigger, pos) then
-						valid = false
-					end
-					--React if time has passed since last sound or if it's substantially stronger
-					if valid and (hearing.timeSinceLastSound > 2.0 or vol > hearing.lastSoundVolume*2.0) then
-						local attenuation = 5.0 / math.max(5.0, dist)
-						attenuation = attenuation * attenuation
-						local heardVolume = vol * attenuation
-						if heardVolume > 0.05 then
-							hearing.lastSoundVolume = vol
-							hearing.lastSoundPos = pos
-							hearing.timeSinceLastSound = 0
-							hearing.hasNewSound = true
-						end
-					end
-				end
-			end
-		end
-
-		function hearingConsumeSound()
-			hearing.hasNewSound = false
-		end
-
-	end
-end
-
-
-
---= OTHER
-do
-	--> Util
-	do
-
-		function truncateToGround(pos)
-			rejectAllBodies(robot.allBodies)
-			QueryRejectVehicle(GetPlayerVehicle())
-			hit, dist = QueryRaycast(pos, Vec(0, -1, 0), 5, 0.2)
-			if hit then
-				pos = VecAdd(pos, Vec(0, -dist, 0))
-			end
-			return pos
-		end
-
-		function getRandomPosInTrigger(trigger)
-			local mi, ma = GetTriggerBounds(trigger)
-			local minDist = math.max(ma[1]-mi[1], ma[3]-mi[3])*0.25
-			minDist = math.min(minDist, 5.0)
-
-			for i=1, 100 do
-				local probe = Vec()
-				for j=1, 3 do
-					probe[j] = mi[j] + (ma[j]-mi[j])*rnd(0,1)
-				end
-				if IsPointInTrigger(trigger, probe) then
-					return probe
-				end
-			end
-			return VecLerp(mi, ma, 0.5)
-		end
-
-		function handleCommand(cmd)
-			words = splitString(cmd, " ")
-			if #words == 5 then
-				if words[1] == "explosion" then
-					local strength = tonumber(words[2])
-					local x = tonumber(words[3])
-					local y = tonumber(words[4])
-					local z = tonumber(words[5])
-					hitByExplosion(strength/2, Vec(x,y,z))
-				end
-			end
-			if #words == 8 then
-				if words[1] == "shot" then
-					local strength = tonumber(words[2])
-					local x = tonumber(words[3])
-					local y = tonumber(words[4])
-					local z = tonumber(words[5])
-					local dx = tonumber(words[6])
-					local dy = tonumber(words[7])
-					local dz = tonumber(words[8])
-					hitByShot(strength/1.5, Vec(x,y,z), Vec(dx,dy,dz))
-				end
-			end
-		end
-
-
-		function getClosestPatrolIndex()
-			local bestIndex = 1
-			local bestDistance = 999
-			for i=1, #patrolLocations do
-				local pt = GetLocationTransform(patrolLocations[i]).pos
-				local d = VecLength(VecSub(pt, robot.transform.pos))
-				if d < bestDistance then
-					bestDistance = d
-					bestIndex = i
-				end
-			end
-			return bestIndex
-		end
-
-
-		function getDistantPatrolIndex(currentPos)
-			local bestIndex = 1
-			local bestDistance = 0
-			for i=1, #patrolLocations do
-				local pt = GetLocationTransform(patrolLocations[i]).pos
-				local d = VecLength(VecSub(pt, currentPos))
-				if d > bestDistance then
-					bestDistance = d
-					bestIndex = i
-				end
-			end
-			return bestIndex
-		end
-
-
-		function getNextPatrolIndex(current)
-			local i = current + 1
-			if i > #patrolLocations then
-				i = 1
-			end
-			return i
-		end
-
-
-		function markPatrolLocationAsActive(index)
-			for i=1, #patrolLocations do
-				if i==index then
-					SetTag(patrolLocations[i], "active")
-				else
-					RemoveTag(patrolLocations[i], "active")
-				end
-			end
-		end
-
-
-		function debugState()
-			local state = stackTop()
-			DebugWatch("state", state.id)
-			DebugWatch("activeTime", state.activeTime)
-			DebugWatch("totalTime", state.totalTime)
-			DebugWatch("navigation.state", navigation.state)
-			DebugWatch("#navigation.path", #navigation.path)
-			DebugWatch("navigation.hasNewTarget", navigation.hasNewTarget)
-			DebugWatch("robot.blocked", robot.blocked)
-			DebugWatch("robot.speed", robot.speed)
-			DebugWatch("navigation.blocked", navigation.blocked)
-			DebugWatch("navigation.unblock", navigation.unblock)
-			DebugWatch("navigation.unblockTimer", navigation.unblockTimer)
-			DebugWatch("navigation.thinkTime", navigation.thinkTime)
-			DebugWatch("GetPathState()", GetPathState())
-		end
-
-
-		function canBeSeenByPlayer()
-			for i=1, #robot.allShapes do
-				if IsShapeVisible(robot.allShapes[i], config.outline, true) then
-					return true
-				end
-			end
-			return false
-		end
-
-		function hitByExplosion(strength, pos)
-			--Explosions smaller than 1.0 are ignored (with a bit of room for rounding errors)
-			if strength > 0.99 then
-				local d = VecDist(pos, robot.bodyCenter)
-				local f = clamp((1.0 - d/10.0), 0.0, 1.0) * strength
-				if f > 0.2 then
-					robot.stunned = robot.stunned + f * 4.0
-				end
-
-				--Give robots an extra push if they are not already moving that much
-				--Unphysical but more fun
-				local maxVel = 7.0
-				local strength = 3.0
-				local dir = VecNormalize(VecSub(robot.bodyCenter, pos))
-				--Tilt direction slightly upwards to make them fly more
-				dir[2] = dir[2] + 0.2
-				dir = VecNormalize(dir)
-				for i=1, #robot.allBodies do
-					local b = robot.allBodies[i]
-					local v = GetBodyVelocity(b)
-					local scale = clamp(1.0-VecLength(v)/maxVel, 0.0, 1.0)
-					local velAdd = math.min(maxVel, f*scale*strength)
-					if velAdd > 0 then
-						v = VecAdd(v, VecScale(dir, velAdd))
-						SetBodyVelocity(b, v)
-					end
-				end
-			end
-		end
-
-
-		function hitByShot(strength, pos, dir)
-			if VecDist(pos, robot.bodyCenter) < 3 then
-				local hit, point, n, shape = QueryClosestPoint(pos, 0.1)
-				if hit then
-					for i=1, #robot.allShapes do
-						if robot.allShapes[i] == shape then
-							robot.stunned = robot.stunned + 0.2
-							return
-						end
-					end
-				end
-			end
-		end
-
-	end
-
-	--> Physics
-	do
-
-		function VecDist(a, b)
-			return VecLength(VecSub(a, b))
-		end
-
-		function rndVec(length)
-			local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
-			return VecScale(v, length)
-		end
-
-		function rnd(mi, ma)
-			local v = math.random(0,1000) / 1000
-			return mi + (ma-mi)*v
-		end
-
-		function rejectAllBodies(bodies)
-			for i=1, #bodies do
-				QueryRejectBody(bodies[i])
-			end
-		end
-
-		function getTagParameter(entity, name, default)
-			local v = tonumber(GetTagValue(entity, name))
-			if v then
-				return v
-			else
-				return default
-			end
-		end
-
-		function getTagParameter2(entity, name, default)
-			local s = splitString(GetTagValue(entity, name), ",")
-			if #s == 1 then
-				local v = tonumber(s[1])
-				if v then
-					return v, v
-				else
-					return default, default
-				end
-			elseif #s == 2 then
-				local v1 = tonumber(s[1])
-				local v2 = tonumber(s[2])
-				if v1 and v2 then
-					return v1, v2
-				else
-					return default, default
-				end
-			else
-				return default, default
-			end
-		end
-
-	end
-
-	--> Logic
-	do
-		stack = {}
-		stack.list = {}
-
-		function stackTop()
-			return stack.list[#stack.list]
-		end
-
-		function stackPush(id)
-			local index = #stack.list+1
-			stack.list[index] = {}
-			stack.list[index].id = id
-			stack.list[index].totalTime = 0
-			stack.list[index].activeTime = 0
-			return stack.list[index]
-		end
-
-		function stackPop(id)
-			if id then
-				while stackHas(id) do
-					stackPop()
-				end
-			else
-				if #stack.list > 1 then
-					stack.list[#stack.list] = nil
-				end
-			end
-		end
-
-		function stackHas(s)
-			return stackGet(s) ~= nil
-		end
-
-		function stackGet(id)
-			for i=1,#stack.list do
-				if stack.list[i].id == id then
-					return stack.list[i]
-				end
-			end
-			return nil
-		end
-
-		function stackClear(s)
-			stack.list = {}
-			stackPush("none")
-		end
-
-		function stackInit()
-			stackClear()
-		end
-
-		function stackUpdate(dt)
-			if #stack.list > 0 then
-				for i=1, #stack.list do
-					stack.list[i].totalTime = stack.list[i].totalTime + dt
-				end
-
-				--Tick total time
-				stack.list[#stack.list].activeTime = stack.list[#stack.list].activeTime + dt
-			end
-		end
-	end
-end
+#version 2

```

---

# Migration Report: custom_robot\scripts\robot_default.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_robot\scripts\robot_default.lua
+++ patched/custom_robot\scripts\robot_default.lua
@@ -1,2206 +1 @@
-#include "camera.lua"
-#include "robot_default_custom.lua"
-#include "debug.lua"
-#include "particles.lua"
-#include "projectiles.lua"
-#include "registry.lua"
-#include "robotPreset.lua"
-#include "script/common.lua"
-#include "sounds.lua"
-#include "timers.lua"
-#include "ui.lua"
-#include "ui_components.lua"
-#include "umf.lua"
-#include "utility.lua"
-#include "version.lua"
-#include "weapons.lua"
-
-
-weaponStatus = "Idle"
-
-
---= MAIN
-do
-	--> Script
-	do
-
-		function init()
-			configInit()
-			robotInit()
-			hoverInit()
-			headInit()
-			sensorInit()
-			wheelsInit()
-			feetInit()
-			aimsInit()
-			weaponsInit()
-			navigationInit()
-			hearingInit()
-			stackInit()
-
-			--> Sound
-			patrolLocations = FindLocations("patrol")
-			shootSound = LoadSound("tools/gun0.ogg", 8.0)
-			rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
-			local nomDist = 7.0
-			if config.stepSound == "s" then nomDist = 5.0 end
-			if config.stepSound == "l" then nomDist = 9.0 end
-			stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
-			headLoop = LoadLoop("robot/head-loop.ogg", 7.0)
-			turnLoop = LoadLoop("robot/turn-loop.ogg", 7.0)
-			walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
-			rollLoop = LoadLoop("robot/roll-loop.ogg", 7.0)
-			chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
-			alertSound = LoadSound("robot/alert.ogg", 9.0)
-			huntSound = LoadSound("robot/hunt.ogg", 9.0)
-			idleSound = LoadSound("robot/idle.ogg", 9.0)
-			fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
-			disableSound = LoadSound("robot/disable0.ogg")
-
-			initCustom() --!
-
-		end
-
-		function update(dt)
-			if robot.deleted then
-				return
-			else
-				if not IsHandleValid(robot.body) then
-					for i=1, #robot.allBodies do
-						Delete(robot.allBodies[i])
-					end
-					for i=1, #robot.allJoints do
-						Delete(robot.allJoints[i])
-					end
-					robot.deleted = true
-				end
-			end
-
-			if robot.activateTrigger ~= 0 then
-				if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform().pos) then
-					RemoveTag(robot.body, "inactive")
-					robot.activateTrigger = 0
-				end
-			end
-
-			if HasTag(robot.body, "inactive") then
-				robot.inactive = true
-				return
-			else
-				if robot.inactive then
-					robot.inactive = false
-					--Reset robot pose
-					local sleep = HasTag(robot.body, "sleeping")
-					for i=1, #robot.allBodies do
-						SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
-						SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
-						SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
-						if sleep then
-							--If robot is sleeping make sure to not wake it up
-							SetBodyActive(robot.allBodies[i], false)
-						end
-					end
-				end
-			end
-
-			if HasTag(robot.body, "sleeping") then
-				if IsBodyActive(robot.body) then
-					wakeUp = true
-				end
-				local vol, pos = GetLastSound()
-				if vol > 0.2 then
-					if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
-						wakeUp = true
-					end
-				end
-				if wakeUp then
-					RemoveTag(robot.body, "sleeping")
-				end
-				return
-			end
-
-			robotUpdate(dt)
-			wheelsUpdate(dt)
-
-			if not robot.enabled then
-				return
-			end
-
-			feetUpdate(dt)
-
-			if IsPointInWater(robot.bodyCenter) then
-				PlaySound(disableSound, robot.bodyCenter)
-				for i=1, #robot.allShapes do
-					SetShapeEmissiveScale(robot.allShapes[i], 0)
-				end
-				SetTag(robot.body, "disabled")
-				robot.enabled = false
-			end
-
-			robot.stunned = clamp(robot.stunned - dt, 0.0, 8.0)
-			if robot.stunned > 0 then
-				Eyes.seenTimer = 0
-				weaponsReset()
-				return
-			end
-
-			hoverUpdate(dt)
-
-			if player.isDrivingRobot then
-				sensorUpdate(dt)
-				headUpdate(dt)
-				aimsUpdate(dt)
-				weaponsUpdate(dt)
-				hearingUpdate(dt)
-				stackUpdate(dt)
-			end
-
-
-			robot.speedScale = 1.5
-			robot.speed = 0
-			-- local state = stackTop()
-			local state = "none"
-
-			if state.id == "none" then
-				-- if config.patrol then
-				-- 	stackPush("patrol")
-				-- else
-				-- 	stackPush("roam")
-				-- end
-			end
-
-			if state.id == "roam" then
-				-- if not state.nextAction then
-				-- 	state.nextAction = "move"
-				-- elseif state.nextAction == "move" then
-				-- 	local randomPos
-				-- 	if robot.roamTrigger ~= 0 then
-				-- 		randomPos = getRandomPosInTrigger(robot.roamTrigger)
-				-- 		randomPos = truncateToGround(randomPos)
-				-- 	else
-				-- 		local rndAng = rnd(0, 2*math.pi)
-				-- 		randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
-				-- 	end
-				-- 	local s = stackPush("navigate")
-				-- 	s.timeout = 1
-				-- 	s.pos = randomPos
-				-- 	state.nextAction = "search"
-				-- elseif state.nextAction == "search" then
-				-- 	stackPush("search")
-				-- 	state.nextAction = "move"
-				-- end
-			end
-
-
-			if state.id == "patrol" then
-				-- if not state.nextAction then
-				-- 	state.index = getClosestPatrolIndex()
-				-- 	state.nextAction = "move"
-				-- elseif state.nextAction == "move" then
-				-- 	markPatrolLocationAsActive(state.index)
-				-- 	local nav = stackPush("navigate")
-				-- 	nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
-				-- 	state.nextAction = "search"
-				-- elseif state.nextAction == "search" then
-				-- 	stackPush("search")
-				-- 	state.index = getNextPatrolIndex(state.index)
-				-- 	state.nextAction = "move"
-				-- end
-			end
-
-
-			if state.id == "search" then
-				if state.activeTime > 2.5 then
-					if not state.turn then
-						robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-						state.turn = true
-					end
-					if state.activeTime > 6.0 then
-						stackPop()
-					end
-				end
-				if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
-					Eyes.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
-				else
-					Eyes.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
-				end
-			end
-
-
-			if state.id == "investigate" then
-				--! disable investigating.
-				-- if not state.nextAction then
-				-- 	local pos = state.pos
-				-- 	robotTurnTowards(state.pos)
-				-- 	headTurnTowards(state.pos)
-				-- 	local nav = stackPush("navigate")
-				-- 	nav.pos = state.pos
-				-- 	nav.timeout = 5.0
-				-- 	state.nextAction = "search"
-				-- elseif state.nextAction == "search" then
-				-- 	stackPush("search")
-				-- 	state.nextAction = "done"
-				-- elseif state.nextAction == "done" then
-				-- 	PlaySound(idleSound, robot.bodyCenter)
-				-- 	stackPop()
-				-- end
-			end
-
-			if state.id == "move" then
-				-- robotTurnTowards(state.pos)
-				-- robot.speed = config.speed
-				-- head.dir = VecCopy(robot.dir)
-				-- local d = VecLength(VecSub(state.pos, robot.transform.pos))
-				-- if d < 2 then
-				-- 	robot.speed = 0
-				-- 	stackPop()
-				-- else
-				-- 	if robot.blocked > 0.5 then
-						-- stackPush("unblock")
-				-- 	end
-				-- end
-			end
-
-			if state.id == "unblock" then
-				-- if not state.dir then
-				-- 	if math.random(0, 10) < 5 then
-				-- 		state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
-				-- 	else
-				-- 		state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
-				-- 	end
-				-- 	state.dir = VecNormalize(state.dir)
-				-- else
-				-- 	robot.dir = state.dir
-				-- 	robot.speed = -math.min(config.speed, 2.0)
-				-- 	if state.activeTime > 1 then
-				-- 		stackPop()
-				-- 	end
-				-- end
-			end
-
-			--Hunt player
-			if state.id == "hunt" then
-				if not state.init then
-					navigationClear()
-					state.init = true
-					state.headAngle = 0
-					state.headAngleTimer = 0
-				end
-				if robot.distToPlayer < 4.0 then
-					robot.dir = VecCopy(robot.dirToPlayer)
-					Eyes.dir = VecCopy(robot.dirToPlayer)
-					robot.speed = 0
-					navigationClear()
-				else
-					navigationSetTarget(Eyes.lastSeenPos, 1.0 + clamp(Eyes.timeSinceLastSeen, 0.0, 4.0))
-					robot.speedScale = config.huntSpeedScale
-					navigationUpdate(dt)
-					if Eyes.canSeePlayer then
-						Eyes.dir = VecCopy(robot.dirToPlayer)
-						state.headAngle = 0
-						state.headAngleTimer = 0
-					else
-						state.headAngleTimer = state.headAngleTimer + dt
-						if state.headAngleTimer > 1.0 then
-							if state.headAngle > 0.0 then
-								state.headAngle = rnd(-1.0, -0.5)
-							elseif state.headAngle < 0 then
-								state.headAngle = rnd(0.5, 1.0)
-							else
-								state.headAngle = rnd(-1.0, 1.0)
-							end
-							state.headAngleTimer = 0
-						end
-						Eyes.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-					end
-				end
-				if navigation.state ~= "move" and Eyes.timeSinceLastSeen < 2 then
-					--Turn towards player if not moving
-					robot.dir = VecCopy(robot.dirToPlayer)
-				end
-				if navigation.state ~= "move" and Eyes.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
-					if VecDist(Eyes.lastSeenPos, robot.bodyCenter) > 3.0 then
-						stackClear()
-						local s = stackPush("investigate")
-						s.pos = VecCopy(Eyes.lastSeenPos)
-					else
-						stackClear()
-						stackPush("huntlost")
-					end
-				end
-			end
-
-			if state.id == "huntlost" then
-				if not state.timer then
-					state.timer = 6
-					state.turnTimer = 1
-				end
-				state.timer = state.timer - dt
-				Eyes.dir = VecCopy(robot.dir)
-				if state.timer < 0 then
-					PlaySound(idleSound, robot.bodyCenter)
-					stackPop()
-				else
-					state.turnTimer = state.turnTimer - dt
-					if state.turnTimer < 0 then
-						robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-						state.turnTimer = rnd(0.5, 1.5)
-					end
-				end
-			end
-
-			--Avoid player
-			if state.id == "avoid" then
-				if not state.init then
-					navigationClear()
-					state.init = true
-					state.headAngle = 0
-					state.headAngleTimer = 0
-				end
-
-				local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform().pos)
-				local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
-				navigationSetTarget(avoidTarget, 1.0)
-				robot.speedScale = config.huntSpeedScale
-				navigationUpdate(dt)
-				if Eyes.canSeePlayer then
-					Eyes.dir = VecNormalize(VecSub(Eyes.lastSeenPos, robot.transform.pos))
-					state.headAngle = 0
-					state.headAngleTimer = 0
-				else
-					state.headAngleTimer = state.headAngleTimer + dt
-					if state.headAngleTimer > 1.0 then
-						if state.headAngle > 0.0 then
-							state.headAngle = rnd(-1.0, -0.5)
-						elseif state.headAngle < 0 then
-							state.headAngle = rnd(0.5, 1.0)
-						else
-							state.headAngle = rnd(-1.0, 1.0)
-						end
-						state.headAngleTimer = 0
-					end
-					Eyes.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-				end
-
-				if navigation.state ~= "move" and Eyes.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
-					stackClear()
-				end
-			end
-
-			--Get up player
-			if state.id == "getup" then
-				if not state.time then
-					state.time = 0
-				end
-				state.time = state.time + dt
-				hover.timeSinceContact = 0
-				if state.time > 1.0 then
-					stackPop()
-				else
-					hoverGetUp()
-				end
-			end
-
-			if state.id == "navigate" then
-				--! disable navigation
-				-- if not state.initialized then
-				-- 	if not state.timeout then state.timeout = 30 end
-				-- 	navigationClear()
-				-- 	navigationSetTarget(state.pos, state.timeout)
-				-- 	state.initialized = true
-				-- else
-				-- 	head.dir = VecCopy(robot.dir)
-				-- 	navigationUpdate(dt)
-				-- 	if navigation.state == "done" or navigation.state == "fail" then
-						stackPop()
-				-- 	end
-				-- end
-			end
-
-			--React to sound
-			if not stackHas("hunt") then
-				if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
-					stackClear()
-					PlaySound(alertSound, robot.bodyCenter)
-					local s = stackPush("investigate")
-					s.pos = hearing.lastSoundPos
-					hearingConsumeSound()
-				end
-			end
-
-			--Seen player
-			if config.huntPlayer and not stackHas("hunt") then
-				if config.canSeePlayer and Eyes.canSeePlayer or robot.canSensePlayer then
-					stackClear()
-					PlaySound(huntSound, robot.bodyCenter)
-					stackPush("hunt")
-				end
-			end
-
-			--Seen player
-			if config.avoidPlayer and not stackHas("avoid") then
-				if config.canSeePlayer and Eyes.canSeePlayer or robot.distToPlayer < 2.0 then
-					stackClear()
-					stackPush("avoid")
-				end
-			end
-
-			--Get up
-			if hover.timeSinceContact > 3.0 and not stackHas("getup") then
-				stackPush("getup")
-			end
-
-			if IsShapeBroken(GetLightShape(Eyes.eye)) then
-				config.hasVision = false
-				config.canSeePlayer = false
-			end
-
-			-- debugState()
-
-			updateCustom(dt)
-		end
-
-		function tick(dt)
-			if not robot.enabled then
-				return
-			end
-
-			if HasTag(robot.body, "turnhostile") then
-				RemoveTag(robot.body, "turnhostile")
-				config.canHearPlayer = true
-				config.canSeePlayer = true
-				config.huntPlayer = true
-				config.aggressive = true
-				config.practice = false
-			end
-
-			--Outline
-			local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform().pos)
-			if dist < config.outline then
-				local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
-				if canBeSeenByPlayer() then
-					a = 0
-				end
-				robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
-				for i=1, #robot.allBodies do
-					DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
-				end
-			end
-
-			--Remove planks and wires after some time
-			local tags = {"plank", "wire"}
-			local removeTimeOut = 10
-			for i=1, #robot.allShapes do
-				local shape = robot.allShapes[i]
-				local joints = GetShapeJoints(shape)
-				for j=1, #joints do
-					local joint = joints[j]
-					for t=1, #tags do
-						local tag = tags[t]
-						if HasTag(joint, tag) then
-							local t = tonumber(GetTagValue(joint, tag)) or 0
-							t = t + dt
-							if t > removeTimeOut then
-								if GetJointType(joint) == "rope" then
-									DetachJointFromShape(joint, shape)
-								else
-									Delete(joint)
-								end
-								break
-							else
-								SetTag(joint, tag, t)
-							end
-						end
-					end
-				end
-			end
-
-			tickCustom(dt)
-
-		end
-
-		function draw()
-			drawCustom()
-		end
-
-	end
-
-	--> Config
-	do
-
-		pType = GetStringParam("type", "")
-		pSpeed = GetFloatParam("speed", 3.5)
-		pTurnSpeed = GetFloatParam("turnspeed", pSpeed)
-
-		config = {}
-		config.hasVision = false
-		config.viewDistance = 25
-		config.viewFov = 150
-		config.canHearPlayer = false
-		config.canSeePlayer = false
-		config.patrol = false
-		config.sensorDist = 5.0
-		config.speed = pSpeed
-		config.turnSpeed = pTurnSpeed
-		config.huntPlayer = false
-		config.huntSpeedScale = 1.6
-		config.avoidPlayer = false
-		config.triggerAlarmWhenSeen = false
-		config.visibilityTimer = 0.3 --Time player must be seen to be identified as enemy (ideal condition)
-		config.lostVisibilityTimer = 5.0 --Time player is seen after losing visibility
-		config.outline = 13
-		config.aimTime = 5.0
-		config.maxSoundDist = 100.0
-		config.aggressive = false
-		config.stepSound = "m"
-		config.practice = false
-
-		PATH_NODE_TOLERANCE = 0.8
-
-		function configInit()
-			local eye = FindLight("eye")
-			local head = FindBody("head")
-			config.patrol = FindLocation("patrol") ~= 0
-			config.hasVision = eye ~= 0
-			config.viewDistance = getTagParameter(eye, "viewdist", config.viewDistance)
-			config.viewFov = getTagParameter(eye, "viewfov", config.viewFov)
-			config.maxSoundDist = getTagParameter(head, "heardist", config.maxSoundDist)
-			if hasWord(pType, "investigate") then
-				config.canHearPlayer = true
-				config.canSeePlayer = true
-			end
-			if hasWord(pType, "chase") then
-				config.canHearPlayer = true
-				config.canSeePlayer = true
-				config.huntPlayer = true
-			end
-			if hasWord(pType, "avoid") and config.patrol then
-				config.avoidPlayer = true
-				config.canSeePlayer = true
-			end
-			if hasWord(pType, "alarm") then
-				config.triggerAlarmWhenSeen = true
-			end
-			if hasWord(pType, "nooutline") then
-				config.outline = 0
-			end
-			if hasWord(pType, "aggressive") then
-				config.aggressive = true
-			end
-			-- if hasWord(pType, "practice") then
-			-- 	config.canSeePlayer = true
-			-- 	config.practice = true
-			-- end
-			local body = FindBody("body")
-			if HasTag(body, "stepsound") then
-				config.stepSound = GetTagValue(body, "stepsound")
-			end
-		end
-
-	end
-
-	--> Navigation
-	do
-
-		navigation = {}
-		navigation.state = "done"
-		navigation.path = {}
-		navigation.target = Vec()
-		navigation.hasNewTarget = false
-		navigation.resultRetrieved = true
-		navigation.deviation = 0		-- Distance to path
-		navigation.blocked = 0
-		navigation.unblockTimer = 0		-- Timer that ticks up when blocked. If reaching limit, unblock kicks in and timer resets
-		navigation.unblock = 0			-- If more than zero, navigation is in unblock mode (reverse direction)
-		navigation.vertical = 0
-		navigation.thinkTime = 0
-		navigation.timeout = 1
-		navigation.lastQueryTime = 0
-		navigation.timeSinceProgress = 0
-
-		function navigationInit()
-			if #wheels.bodies > 0 then
-				navigation.pathType = "low"
-			else
-				navigation.pathType = "standard"
-			end
-		end
-
-		--Prune path backwards so robot don't need to go backwards
-		function navigationPrunePath()
-			if #navigation.path > 0 then
-				for i=#navigation.path, 1, -1 do
-					local p = navigation.path[i]
-					local dv = VecSub(p, robot.transform.pos)
-					local d = VecLength(dv)
-					if d < PATH_NODE_TOLERANCE then
-						--Keep everything after this node and throw out the rest
-						local newPath = {}
-						for j=i, #navigation.path do
-							newPath[#newPath+1] = navigation.path[j]
-						end
-						navigation.path = newPath
-						return
-					end
-				end
-			end
-		end
-
-		function navigationClear()
-			AbortPath()
-			navigation.state = "done"
-			navigation.path = {}
-			navigation.hasNewTarget = false
-			navigation.resultRetrieved = true
-			navigation.deviation = 0
-			navigation.blocked = 0
-			navigation.unblock = 0
-			navigation.vertical = 0
-			navigation.target = Vec(0, -100, 0)
-			navigation.thinkTime = 0
-			navigation.lastQueryTime = 0
-			navigation.unblockTimer = 0
-			navigation.timeSinceProgress = 0
-		end
-
-		function navigationSetTarget(pos, timeout)
-			pos = truncateToGround(pos)
-			if VecDist(navigation.target, pos) > 0 then
-				navigation.target = VecCopy(pos)
-				navigation.hasNewTarget = true
-				navigation.state = "move"
-			end
-			navigation.timeout = timeout
-			navigation.timeSinceProgress = 0
-		end
-
-		function navigationUpdate(dt)
-			if GetPathState() == "busy" then
-				navigation.timeSinceProgress = 0
-				navigation.thinkTime = navigation.thinkTime + dt
-				if navigation.thinkTime > navigation.timeout then
-					AbortPath()
-				end
-			end
-
-			if GetPathState() ~= "busy" then
-				if GetPathState() == "done" or GetPathState() == "fail" then
-					if not navigation.resultRetrieved then
-						if GetPathLength() > 0.5 then
-							for l=0.2, GetPathLength(), 0.2 do
-								navigation.path[#navigation.path+1] = GetPathPoint(l)
-							end
-						end
-						navigation.lastQueryTime = navigation.thinkTime
-						navigation.resultRetrieved = true
-						navigation.state = "move"
-						navigationPrunePath()
-					end
-				end
-				navigation.thinkTime = 0
-			end
-
-			if navigation.thinkTime == 0 and navigation.hasNewTarget then
-				local startPos
-
-				if #navigation.path > 0 and VecDist(navigation.path[1], robot.navigationCenter) < 2.0 then
-					--Keep a little bit of the old path and use last point of that as start position
-					--Use previous query's time as an estimate for the next
-					local distToKeep = VecLength(GetBodyVelocity(robot.body))*navigation.lastQueryTime
-					local nodesToKeep = math.clamp(math.ceil(distToKeep / 0.2), 1, 15)
-					local newPath = {}
-					for i=1, math.min(nodesToKeep, #navigation.path) do
-						newPath[i] = navigation.path[i]
-					end
-					navigation.path = newPath
-					startPos = navigation.path[#navigation.path]
-				else
-					startPos = truncateToGround(robot.transform.pos)
-					navigation.path = {}
-				end
-
-				local targetRadius = 1.0
-				if GetPlayerVehicle()~=0 then
-					targetRadius = 4.0
-				end
-
-				local target = navigation.target
-				-- if robot.limitTrigger ~= 0 then
-				-- 	target = GetTriggerClosestPoint(robot.limitTrigger, target)
-					target = truncateToGround(target)
-				-- end
-
-				QueryRequire("physical large")
-				rejectAllBodies(robot.allBodies)
-				QueryPath(startPos, target, 100, targetRadius, navigation.pathType)
-
-				navigation.timeSinceProgress = 0
-				navigation.hasNewTarget = false
-				navigation.resultRetrieved = false
-				navigation.state = "move"
-			end
-
-			navigationMove(dt)
-
-			if GetPathState() ~= "busy" and #navigation.path == 0 and not navigation.hasNewTarget then
-				if GetPathState() == "done" or GetPathState() == "idle" then
-					navigation.state = "done"
-				else
-					navigation.state = "fail"
-				end
-			end
-		end
-
-		function navigationMove(dt)
-			if #navigation.path > 0 then
-				if navigation.resultRetrieved then
-					--If we have a finished path and didn't progress along it for five seconds, recompute
-					--Should probably only do this for a limited time until giving up
-					navigation.timeSinceProgress = navigation.timeSinceProgress + dt
-					if navigation.timeSinceProgress > 5.0 then
-						navigation.hasNewTarget = true
-						navigation.path = {}
-					end
-				end
-				if navigation.unblock > 0 then
-					robot.speed = -2
-					navigation.unblock = navigation.unblock - dt
-				else
-					local target = navigation.path[1]
-					local dv = VecSub(target, robot.navigationCenter)
-					local distToFirstPathPoint = VecLength(dv)
-					dv[2] = 0
-					local d = VecLength(dv)
-					if distToFirstPathPoint < 2.5 then
-						if d < PATH_NODE_TOLERANCE then
-							if #navigation.path > 1 then
-								--Measure verticality which should decrease speed
-								local diff = VecSub(navigation.path[2], navigation.path[1])
-								navigation.vertical = diff[2] / (VecLength(diff)+0.001)
-								--Remove the first one
-								local newPath = {}
-								for i=2, #navigation.path do
-									newPath[#newPath+1] = navigation.path[i]
-								end
-								navigation.path = newPath
-								navigation.timeSinceProgress = 0
-							else
-								--We're done
-								navigation.path = {}
-								robot.speed = 0
-								return
-							end
-						else
-							--Walk towards first point on path
-							robot.dir = VecCopy(VecNormalize(VecSub(target, robot.transform.pos)))
-
-							local dirDiff = VecDot(VecScale(robot.axes[3], -1), robot.dir)
-							local speedScale = math.max(0.25, dirDiff)
-							speedScale = speedScale * clamp(1.0 - navigation.vertical, 0.3, 1.0)
-							robot.speed = config.speed * speedScale
-
-						end
-					else
-						--Went off path, scrap everything and recompute
-						navigation.hasNewTarget = true
-						navigation.path = {}
-					end
-
-					--Check if stuck
-					-- if robot.blocked > 0.2 then
-					-- 	navigation.blocked = navigation.blocked + dt
-					-- 	if navigation.blocked > 0.2 then
-					-- 		robot.breakAllTimer = 0.1
-					-- 		navigation.blocked = 0.0
-					-- 	end
-					-- 	navigation.unblockTimer = navigation.unblockTimer + dt
-					-- 	if navigation.unblockTimer > 2.0 and navigation.unblock <= 0.0 then
-					-- 		navigation.unblock = 1.0
-					-- 		navigation.unblockTimer = 0
-					-- 	end
-					-- else
-					-- 	navigation.blocked = 0
-					-- 	navigation.unblockTimer = 0
-					-- end
-				end
-			end
-		end
-
-	end
-
-end
-
-
-
---= ROBOT
-do
-	--> Robot
-	do
-
-		robot = {}
-		robot.body = 0
-		robot.transform = Transform()
-		robot.axes = {}
-		robot.bodyCenter = Vec()
-		robot.navigationCenter = Vec()
-		robot.dir = Vec(0, 0, -1)
-		robot.speed = 0
-		robot.blocked = 0
-		robot.mass = 0
-		robot.allBodies = {}
-		robot.allShapes = {}
-		robot.allJoints = {}
-		robot.initialBodyTransforms = {}
-		robot.enabled = true
-		robot.deleted = false
-		robot.speedScale = 1
-		robot.breakAll = false
-		robot.breakAllTimer = 0
-		robot.distToPlayer = 100
-		robot.dirToPlayer = 0
-		robot.roamTrigger = 0
-		robot.limitTrigger = 0
-		robot.investigateTrigger = 0
-		robot.activateTrigger = 0
-		robot.stunned = 0
-		robot.outlineAlpha = 0
-		robot.canSensePlayer = false
-		robot.playerPos = Vec()
-
-
-		function robotSetAxes()
-			robot.transform = GetBodyTransform(robot.body)
-			robot.axes[1] = TransformToParentVec(robot.transform, Vec(1, 0, 0))
-			robot.axes[2] = TransformToParentVec(robot.transform, Vec(0, 1, 0))
-			robot.axes[3] = TransformToParentVec(robot.transform, Vec(0, 0, 1))
-		end
-
-
-		function robotInit()
-			robot.body = FindBody("body")
-			robot.allBodies = FindBodies()
-			robot.allShapes = FindShapes()
-			robot.allJoints = FindJoints()
-			robot.roamTrigger = FindTrigger("roam")
-			robot.limitTrigger = FindTrigger("limit")
-			robot.investigateTrigger = FindTrigger("investigate")
-			robot.activateTrigger = FindTrigger("activate")
-			if robot.activateTrigger ~= 0 then
-				SetTag(robot.body, "inactive")
-			end
-			for i=1, #robot.allBodies do
-				robot.initialBodyTransforms[i] = GetBodyTransform(robot.allBodies[i])
-			end
-			robotSetAxes()
-		end
-
-
-		function robotTurnTowards(pos)
-			robot.dir = VecNormalize(VecSub(pos, robot.transform.pos))
-		end
-
-
-		function robotSetDirAngle(angle)
-			robot.dir[1] = math.cos(angle)
-			robot.dir[3] = math.sin(angle)
-		end
-
-
-		function robotGetDirAngle()
-			return math.atan2(robot.dir[3], robot.dir[1])
-		end
-
-
-		function robotUpdate(dt)
-			robotSetAxes()
-
-			-- if config.practice then
-			-- 	local overrideTarget = FindBody("practicetarget", true)
-			-- 	if overrideTarget ~= 0 then
-			-- 		robot.playerPos = GetBodyTransform(overrideTarget).pos
-			-- 		if not stackHas("navigate") then
-			-- 			robotTurnTowards(robot.playerPos)
-			-- 		end
-			-- 	else
-			-- 		robot.playerPos = Vec(0, -100, 0)
-			-- 	end
-			-- else
-				robot.playerPos = getOuterCrosshairWorldPos()
-			-- end
-
-			-- local vel = GetBodyVelocity(robot.body)
-			-- local fwdSpeed = VecDot(vel, robot.dir)
-			-- local blocked = 0
-			-- if robot.speed > 0 and fwdSpeed > -0.1 then
-			-- 	blocked = 1.0 - clamp(fwdSpeed/0.5, 0.0, 1.0)
-			-- end
-			-- robot.blocked = robot.blocked * 0.95 + blocked * 0.05
-
-			--Always blocked if fall is detected
-			-- if sensor.detectFall > 0 then
-			-- 	robot.blocked = 1.0
-			-- end
-
-			--Evaluate mass every frame since robots can break
-			robot.mass = 0
-			local bodies = FindBodies()
-			for i=1, #bodies do
-				robot.mass = robot.mass + GetBodyMass(bodies[i])
-			end
-
-			robot.bodyCenter = TransformToParentPoint(robot.transform, GetBodyCenterOfMass(robot.body))
-			robot.navigationCenter = TransformToParentPoint(robot.transform, Vec(0, -hover.distTarget, 0))
-
-			--Handle break all
-			robot.breakAllTimer = math.max(0.0, robot.breakAllTimer - dt)
-			if not robot.breakAll and robot.breakAllTimer > 0.0 then
-				for i=1, #robot.allShapes do
-					SetTag(robot.allShapes[i], "breakall")
-				end
-				robot.breakAll = true
-			end
-			if robot.breakAll and robot.breakAllTimer <= 0.0 then
-				for i=1, #robot.allShapes do
-					RemoveTag(robot.allShapes[i], "breakall")
-				end
-				robot.breakAll = false
-			end
-
-			--Distance and direction to player
-			local pp = VecAdd(GetPlayerTransform().pos, Vec(0, 1, 0))
-			local d = VecSub(pp, robot.bodyCenter)
-			robot.distToPlayer = VecLength(d)
-			robot.dirToPlayer = VecScale(d, 1.0/robot.distToPlayer)
-
-
-			--Sense player if player is close and there is nothing in between
-			robot.canSensePlayer = false
-			if robot.distToPlayer < 3.0 then
-				rejectAllBodies(robot.allBodies)
-				if not QueryRaycast(robot.bodyCenter, robot.dirToPlayer, robot.distToPlayer) then
-					robot.canSensePlayer = true
-				end
-			end
-
-			--Robot body sounds
-			if robot.enabled and hover.contact > 0 then
-				local vol
-				vol = clamp(VecLength(GetBodyVelocity(robot.body)) * 0.4, 0.0, 1.0)
-				if vol > 0 then
-					PlayLoop(walkLoop, robot.transform.pos, vol)
-				end
-
-				vol = clamp(VecLength(GetBodyAngularVelocity(robot.body)) * 0.4, 0.0, 1.0)
-				if vol > 0 then
-					PlayLoop(turnLoop, robot.transform.pos, vol)
-				end
-			end
-		end
-
-	end
-
-	--> Head
-	do
-
-		Eyes = {}
-		Eyes.body = 0
-		Eyes.eye = 0
-		Eyes.dir = Vec(0,0,-1)
-		Eyes.lookOffset = 0
-		Eyes.lookOffsetTimer = 0
-		Eyes.canSeePlayer = false
-		Eyes.lastSeenPos = Vec(0,0,0)
-		Eyes.timeSinceLastSeen = 999
-		Eyes.seenTimer = 0
-		Eyes.alarmTimer = 0
-		Eyes.alarmTime = 2.0
-		Eyes.aim = 0	-- 1.0 = perfect aim, 0.0 = will always miss player. This increases when robot sees player based on config.aimTime
-
-		function headInit()
-			Eyes.body = FindBody("head")
-			Eyes.eye = FindLight("eye")
-			Eyes.joint = FindJoint("head")
-			Eyes.alarmTime = getTagParameter(Eyes.eye, "alarm", 2.0)
-		end
-
-		function headTurnTowards(pos)
-			Eyes.dir = VecNormalize(VecSub(pos, GetBodyTransform(Eyes.body).pos))
-		end
-
-		function headUpdate(dt)
-			local t = GetBodyTransform(Eyes.body)
-			local fwd = TransformToParentVec(t, Vec(0, 0, -1))
-
-			--Check if head can see player
-			local et = GetLightTransform(Eyes.eye)
-			local pp = VecCopy(robot.playerPos)
-			local toPlayer = VecSub(pp, et.pos)
-			local distToPlayer = VecLength(toPlayer)
-			toPlayer = VecNormalize(toPlayer)
-
-			--Determine player visibility
-			local playerVisible = false
-			if config.hasVision and config.canSeePlayer then
-				if distToPlayer < config.viewDistance then	--Within view distance
-					local limit = math.cos(config.viewFov * 0.5 * math.pi / 180)
-					if VecDot(toPlayer, fwd) > limit then --In view frustum
-						rejectAllBodies(robot.allBodies)
-						QueryRejectVehicle(GetPlayerVehicle())
-						if not QueryRaycast(et.pos, toPlayer, distToPlayer, 0, true) then --Not blocked
-							playerVisible = true
-						end
-					end
-				end
-			end
-
-			if config.aggressive then
-				playerVisible = true
-			end
-
-			--If player is visible it takes some time before registered as seen
-			--If player goes out of sight, head can still see for some time second (approximation of motion estimation)
-			if playerVisible then
-				local distanceScale = clamp(1.0 - distToPlayer/config.viewDistance, 0.5, 1.0)
-				local angleScale = clamp(VecDot(toPlayer, fwd), 0.5, 1.0)
-				local delta = (dt * distanceScale * angleScale) / (config.visibilityTimer / 0.5)
-				Eyes.seenTimer = math.min(1.0, Eyes.seenTimer + delta)
-			else
-				Eyes.seenTimer = math.max(0.0, Eyes.seenTimer - dt / config.lostVisibilityTimer)
-			end
-			Eyes.canSeePlayer = (Eyes.seenTimer > 0.5)
-
-			if Eyes.canSeePlayer then
-				Eyes.lastSeenPos = pp
-				Eyes.timeSinceLastSeen = 0
-			else
-				Eyes.timeSinceLastSeen = Eyes.timeSinceLastSeen + dt
-			end
-
-			if playerVisible and Eyes.canSeePlayer then
-				Eyes.aim = math.min(1.0, Eyes.aim + dt / config.aimTime)
-			else
-				Eyes.aim = math.max(0.0, Eyes.aim - dt / config.aimTime)
-			end
-
-			if config.triggerAlarmWhenSeen then
-				local red = false
-				if GetBool("level.alarm") then
-					red = math.mod(GetTime(), 0.5) > 0.25
-				else
-					if playerVisible and IsPointAffectedByLight(Eyes.eye, pp) then
-						red = true
-						Eyes.alarmTimer = Eyes.alarmTimer + dt
-						PlayLoop(chargeLoop, robot.transform.pos)
-						if Eyes.alarmTimer > Eyes.alarmTime and playerVisible then
-							SetBool("level.alarm", true)
-						end
-					else
-						Eyes.alarmTimer = math.max(0.0, Eyes.alarmTimer - dt)
-					end
-				end
-				if red then
-					SetLightColor(Eyes.eye, 1, 0, 0)
-				else
-					SetLightColor(Eyes.eye, 1, 1, 1)
-				end
-			end
-
-			--Rotate head to head.dir
-			local fwd = TransformToParentVec(t, Vec(0, 0, -1))
-			if playerVisible then
-				headTurnTowards(pp)
-			end
-			Eyes.dir = VecNormalize(Eyes.dir)
-			--end
-			local c = VecCross(fwd, Eyes.dir)
-			local d = VecDot(c, robot.axes[2])
-			local angVel = clamp(d*10, -3, 3)
-			local f = 100
-			mi, ma = GetJointLimits(Eyes.joint)
-			local ang = GetJointMovement(Eyes.joint)
-			if ang < mi+1 and angVel < 0 then
-				angVel = 0
-			end
-			if ang > ma-1 and angVel > 0 then
-				angVel = 0
-			end
-
-			ConstrainAngularVelocity(Eyes.body, robot.body, robot.axes[2], angVel, -f , f)
-
-			local vol = clamp(math.abs(angVel)*0.3, 0.0, 1.0)
-			if vol > 0 then
-				PlayLoop(headLoop, robot.transform.pos, vol)
-			end
-		end
-
-	end
-
-	--> Feet
-	do
-		feet = {}
-
-		function feetInit()
-			local f = FindBodies("foot")
-			for i=1, #f do
-				local foot = {}
-				foot.body = f[i]
-				local t = GetBodyTransform(foot.body)
-				local rayOrigin = TransformToParentPoint(t, Vec(0, 0.9, 0))
-				local rayDir = TransformToParentVec(t, Vec(0, -1, 0))
-
-				foot.lastTransform = TransformCopy(t)
-				foot.targetTransform = TransformCopy(t)
-				foot.candidateTransform = TransformCopy(t)
-				foot.worldTransform = TransformCopy(t)
-				foot.stepAge = 1
-				foot.stepLifeTime = 1
-				foot.localRestTransform = TransformToLocalTransform(robot.transform, t)
-				foot.localTransform = TransformCopy(foot.localRestTransform)
-				foot.rayOrigin = TransformToLocalPoint(robot.transform, rayOrigin)
-				foot.rayDir = TransformToLocalVec(robot.transform, rayDir)
-				foot.rayDist = hover.distTarget + hover.distPadding
-				foot.contact = true
-				local mass = GetBodyMass(foot.body)
-				foot.linForce = 20 * mass
-				foot.angForce = 1 * mass
-				local linScale, angScale = getTagParameter2(foot.body, "force", 1.0)
-				foot.linForce = foot.linForce * linScale
-				foot.angForce = foot.angForce * angScale
-				feet[i] = foot
-			end
-		end
-
-
-		function feetCollideLegs(enabled)
-			local mask = 0
-			if enabled then
-				mask = 253
-			end
-			local feet = FindBodies("foot")
-			for i=1, #feet do
-				local shapes = GetBodyShapes(feet[i])
-				for j=1, #shapes do
-					SetShapeCollisionFilter(shapes[j], 2, mask)
-				end
-			end
-			local legs = FindBodies("leg")
-			for i=1, #legs do
-				local shapes = GetBodyShapes(legs[i])
-				for j=1, #shapes do
-					SetShapeCollisionFilter(shapes[j], 2, mask)
-				end
-			end
-			for i=1, #wheels.bodies do
-				local shapes = GetBodyShapes(wheels.bodies[i])
-				for j=1, #shapes do
-					SetShapeCollisionFilter(shapes[j], 2, mask)
-				end
-			end
-		end
-
-
-		function feetUpdate(dt)
-			if robot.stunned > 0 then
-				feetCollideLegs(true)
-				return
-			else
-				feetCollideLegs(false)
-			end
-
-			local vel = GetBodyVelocity(robot.body)
-			local velLength = VecLength(vel)
-			local stepLength = clamp(velLength*1.5, 0.5, 1)
-			local stepTime = math.min(stepLength / velLength * 0.5, 0.25)
-			local stepHeight = stepLength * 0.5
-
-			local inStep = false
-			for i=1, #feet do
-
-				local q = feet[i].stepAge/feet[i].stepLifeTime
-				if feet[i].stepLifeTime > stepTime then
-					feet[i].stepLifeTime = stepTime
-				end
-				if q < 0.8 then
-					inStep = true
-				end
-			end
-
-			for i=1, #feet do
-				local foot = feet[i]
-
-				if not inStep then
-					--Find candidate footstep
-					local tPredict = TransformCopy(robot.transform)
-					tPredict.pos = VecAdd(tPredict.pos, VecScale(VecLerp(VecScale(robot.dir, robot.speed), vel, 0.5), stepTime*1.5))
-					local rayOrigin = TransformToParentPoint(tPredict, foot.rayOrigin)
-					local rayDir = TransformToParentVec(tPredict, foot.rayDir)
-					QueryRequire("physical large")
-					rejectAllBodies(robot.allBodies)
-					local hit, dist, normal, shape = QueryRaycast(rayOrigin, rayDir, foot.rayDist)
-					local targetTransform = TransformToParentTransform(robot.transform, foot.localRestTransform)
-					if hit then
-						targetTransform.pos = VecAdd(rayOrigin, VecScale(rayDir, dist))
-					end
-					foot.candidateTransform = targetTransform
-				end
-
-				--Animate foot
-				if hover.contact > 0 then
-					if foot.stepAge < foot.stepLifeTime then
-						foot.stepAge = math.min(foot.stepAge + dt, foot.stepLifeTime)
-						local q = foot.stepAge / foot.stepLifeTime
-						q = q * q * (3.0 - 2.0 * q) -- smoothstep
-						local p = VecLerp(foot.lastTransform.pos, foot.targetTransform.pos, q)
-						p[2] = p[2] + math.sin(math.pi * q)*stepHeight
-						local r = QuatSlerp(foot.lastTransform.rot, foot.targetTransform.rot, q)
-						foot.worldTransform = Transform(p, r)
-						foot.localTransform = TransformToLocalTransform(robot.transform, foot.worldTransform)
-						if foot.stepAge == foot.stepLifeTime then
-							PlaySound(stepSound, p, 0.5)
-						end
-					end
-					ConstrainPosition(foot.body, robot.body, GetBodyTransform(foot.body).pos, foot.worldTransform.pos, 8, foot.linForce)
-					ConstrainOrientation(foot.body, robot.body, GetBodyTransform(foot.body).rot, foot.worldTransform.rot, 16, foot.angForce)
-				end
-
-			end
-
-			if not inStep then
-				--Find best step candidate
-				local bestFoot = 0
-				local bestDist = 0
-				for i=1, #feet do
-					local foot = feet[i]
-					local dist = VecLength(VecSub(foot.targetTransform.pos, foot.candidateTransform.pos))
-					if dist > stepLength and dist > bestDist then
-						bestDist = dist
-						bestFoot = i
-					end
-				end
-				--Initiate best footstep
-				if bestFoot ~= 0 then
-					local foot = feet[bestFoot]
-					foot.lastTransform = TransformCopy(GetBodyTransform(foot.body))
-					foot.targetTransform = TransformCopy(foot.candidateTransform)
-					foot.stepAge = 0
-					foot.stepLifeTime = stepTime
-				end
-			end
-		end
-	end
-
-	--> Hover
-	do
-
-		hover = {}
-		hover.hitBody = 0
-		hover.contact = 0.0
-		hover.distTarget = 0.3
-		hover.distPadding = 0.3
-		hover.timeSinceContact = 0.0
-
-
-		function hoverInit()
-			local bodyPos = robot.transform.pos
-			local footMin, footMax = GetBodyBounds(FindBodies('foot')[1])
-			local dist = bodyPos[2] - footMin[2]
-
-			-- local maxDist = 2.0
-			-- local hit, dist = QueryRaycast(robot.transform.pos, VecScale(robot.axes[2], -1), maxDist)
-			-- if hit then
-				hover.distTarget = dist
-				hover.distPadding = math.min(0.3, dist*0.5)
-			-- end
-		end
-
-
-		function hoverFloat()
-			if hover.contact > 0 then
-				local d = clamp(hover.distTarget - hover.currentDist, -0.2, 0.2)
-				local v = d * 10
-				local f = hover.contact * math.max(0, d*robot.mass*5.0) + robot.mass*0.2
-				ConstrainVelocity(robot.body, hover.hitBody, robot.bodyCenter, Vec(0,1,0), v, 0 , f)
-			end
-		end
-
-
-		UPRIGHT_STRENGTH = 1.0	-- Spring strength
-		UPRIGHT_MAX = 0.5		-- Max spring force
-		UPRIGHT_BASE = 0.1		-- Fraction of max spring force to always apply (less springy)
-		function hoverUpright()
-			local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
-			axes = {}
-			axes[1] = Vec(1,0,0)
-			axes[2] = Vec(0,1,0)
-			axes[3] = Vec(0,0,1)
-			for a = 1, 3, 2 do
-				local d = VecDot(up, axes[a])
-				local v = math.clamp(d * 15, -2, 2)
-				local f = math.clamp(math.abs(d)*UPRIGHT_STRENGTH, -UPRIGHT_MAX, UPRIGHT_MAX)
-				f = f + UPRIGHT_MAX * UPRIGHT_BASE
-				f = f * robot.mass
-				f = f * hover.contact
-				--f = 10000
-				ConstrainAngularVelocity(robot.body, hover.hitBody, axes[a], v, -f , f)
-			end
-		end
-
-
-		function hoverGetUp()
-			local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
-			axes = {}
-			axes[1] = Vec(1,0,0)
-			axes[2] = Vec(0,1,0)
-			axes[3] = Vec(0,0,1)
-			for a = 1, 3, 2 do
-				local d = VecDot(up, axes[a])
-				local v = math.clamp(d * 15, -2, 2)
-				local f = math.clamp(math.abs(d)*UPRIGHT_STRENGTH, -UPRIGHT_MAX, UPRIGHT_MAX)
-				f = f + UPRIGHT_MAX * UPRIGHT_BASE
-				f = f * robot.mass
-				ConstrainAngularVelocity(robot.body, hover.hitBody, axes[a], v, -f , f)
-			end
-		end
-
-
-		function hoverTurn()
-			local fwd = VecScale(robot.axes[3], -1)
-			local c = VecCross(fwd, robot.dir)
-			local d = VecDot(c, robot.axes[2])
-			local angVel = clamp(d*10, -config.turnSpeed * robot.speedScale, config.turnSpeed * robot.speedScale)
-
-			local curr = VecDot(robot.axes[2], GetBodyAngularVelocity(robot.body))
-			angVel = curr + clamp(angVel - curr, -0.2*robot.speedScale, 0.2*robot.speedScale)
-
-			-- local f = robot.mass*0.5 * hover.contact
-			local f = robot.mass*0.5 * hover.contact
-			ConstrainAngularVelocity(robot.body, hover.hitBody, robot.axes[2], angVel, -f , f)
-		end
-
-
-		function hoverMove()
-			local desiredSpeed = robot.speed * robot.speedScale
-			local fwd = VecScale(robot.axes[3], -1)
-			fwd[2] = 0
-			fwd = VecNormalize(fwd)
-			local side = VecCross(Vec(0,1,0), fwd)
-			local currSpeed = VecDot(fwd, GetBodyVelocityAtPos(robot.body, robot.bodyCenter))
-			local speed = currSpeed + clamp(desiredSpeed - currSpeed/2, -0.05*robot.speedScale, 0.05*robot.speedScale)
-			local f = robot.mass*0.2 * hover.contact
-
-			ConstrainVelocity(robot.body, hover.hitBody, robot.bodyCenter, fwd, speed, -f , f)
-			ConstrainVelocity(robot.body, hover.hitBody, robot.bodyCenter, robot.axes[1], 0, -f , f)
-		end
-
-
-		BALANCE_RADIUS = 0.4
-		function hoverUpdate(dt)
-			local dir = VecScale(robot.axes[2], -1)
-
-			--Shoot rays from four locations downwards
-			local hit = false
-			local dist = 0
-			local normal = Vec(0,0,0)
-			local shape = 0
-			local samples = {}
-			samples[#samples+1] = Vec(-BALANCE_RADIUS,0,0)
-			samples[#samples+1] = Vec(BALANCE_RADIUS,0,0)
-			samples[#samples+1] = Vec(0,0,BALANCE_RADIUS)
-			samples[#samples+1] = Vec(0,0,-BALANCE_RADIUS)
-			local castRadius = 0.1
-			local maxDist = hover.distTarget + hover.distPadding
-			for i=1, #samples do
-				QueryRequire("physical large")
-				rejectAllBodies(robot.allBodies)
-				local origin = TransformToParentPoint(robot.transform, samples[i])
-				local rhit, rdist, rnormal, rshape = QueryRaycast(origin, dir, maxDist, castRadius)
-				if rhit then
-					hit = true
-					dist = dist + rdist + castRadius
-					if rdist == 0 then
-						--Raycast origin in geometry, normal unsafe. Assume upright
-						rnormal = Vec(0,1,0)
-					end
-					if shape == 0 then
-						shape = rshape
-					else
-						local b = GetShapeBody(rshape)
-						local bb = GetShapeBody(shape)
-						--Prefer new hit if it's static or has more mass than old one
-						if not IsBodyDynamic(b) or (IsBodyDynamic(bb) and GetBodyMass(b) > GetBodyMass(bb)) then
-							shape = rshape
-						end
-					end
-					normal = VecAdd(normal, rnormal)
-				else
-					dist = dist + maxDist
-				end
-			end
-
-			--Use average of rays to determine contact and height
-			if hit then
-				dist = dist / #samples
-				normal = VecNormalize(normal)
-				hover.hitBody = GetShapeBody(shape)
-				if IsBodyDynamic(hover.hitBody) and GetBodyMass(hover.hitBody) < 300 then
-					--Hack alert! Treat small bodies as static to avoid sliding and glitching around on debris
-					hover.hitBody = 0
-				end
-				hover.currentDist = dist
-				hover.contact = clamp(1.0 - (dist - hover.distTarget) / hover.distPadding, 0.0, 1.0)
-				hover.contact = hover.contact * math.max(0, normal[2])
-			else
-				hover.hitBody = 0
-				hover.currentDist = maxDist
-				hover.contact = 0
-			end
-
-			--Limit body angular velocity magnitude to 10 rad/s at max contact
-			if hover.contact > 0 then
-				local maxAngVel = 10.0 / hover.contact
-				local angVel = GetBodyAngularVelocity(robot.body)
-				local angVelLength = VecLength(angVel)
-				if angVelLength > maxAngVel then
-					SetBodyAngularVelocity(robot.body, VecScale(maxAngVel / angVelLength))
-				end
-			end
-
-			if hover.contact > 0 then
-				hover.timeSinceContact = 0
-			else
-				hover.timeSinceContact = hover.timeSinceContact + dt
-			end
-
-			hoverFloat()
-			hoverUpright()
-			hoverTurn()
-			hoverMove()
-		end
-
-	end
-
-	--> Wheels
-	do
-
-		wheels = {}
-		wheels.bodies = {}
-		wheels.transforms = {}
-		wheels.radius = {}
-
-		function wheelsInit()
-			wheels.bodies = FindBodies("wheel")
-			for i=1, #wheels.bodies do
-				local t = GetBodyTransform(wheels.bodies[i])
-				local shape = GetBodyShapes(wheels.bodies[i])[1]
-				local sx, sy, sz = GetShapeSize(shape)
-				wheels.transforms[i] = TransformToLocalTransform(robot.transform, t)
-				wheels.radius[i] = math.max(sx, sz)*0.05
-			end
-		end
-
-		function wheelsUpdate(dt)
-			for i=1, #wheels.bodies do
-				local v = GetBodyVelocityAtPos(robot.body, TransformToParentPoint(robot.transform, wheels.transforms[i].pos))
-				local lv = VecDot(robot.axes[3], v)
-				if hover.contact > 0 then
-					local shapes = GetBodyShapes(wheels.bodies[i])
-					if #shapes > 0 then
-						local joints = GetShapeJoints(shapes[1])
-						if #joints > 0 then
-							local angVel = lv / wheels.radius[i]
-							SetJointMotor(joints[1], angVel, 100)
-						end
-					end
-					PlayLoop(rollLoop, robot.transform.pos, clamp(math.abs(lv)*0.5, 0.0, 1.0))
-				end
-			end
-		end
-
-	end
-
-	--> Weapons
-	do
-
-		weapons = {}
-
-		function weaponsInit()
-			local locs = FindLocations("weapon")
-			for i=1, #locs do
-				local loc = locs[i]
-				local t = GetLocationTransform(loc)
-				QueryRequire("dynamic large")
-				local hit, point, normal, shape = QueryClosestPoint(t.pos, 0.15)
-				if hit then
-					local weapon = {}
-					weapon.type = GetTagValue(loc, "weapon")
-					weapon.timeBetweenRounds = tonumber(GetTagValue(loc, "idle"))
-					weapon.chargeTime = tonumber(GetTagValue(loc, "charge"))
-					weapon.fireCooldown = tonumber(GetTagValue(loc, "cooldown"))
-					weapon.shotsPerRound = tonumber(GetTagValue(loc, "count"))
-					weapon.spread = tonumber(GetTagValue(loc, "spread"))
-					weapon.strength = tonumber(GetTagValue(loc, "strength"))
-					weapon.maxDist = tonumber(GetTagValue(loc, "maxdist"))
-					if weapon.type == "" then weapon.type = "gun" end
-					if not weapon.timeBetweenRounds then weapon.timeBetweenRounds = 1 end
-					if not weapon.chargeTime then weapon.chargeTime = 1.2 end
-					if not weapon.fireCooldown then weapon.fireCooldown = 0.15 end
-					if not weapon.shotsPerRound then weapon.shotsPerRound = 8 end
-					if not weapon.spread then weapon.spread = 0.01 end
-					if not weapon.strength then weapon.strength = 1.0 end
-					if not weapon.maxDist then weapon.maxDist = 100.0 end
-					local b = GetShapeBody(shape)
-					local bt = GetBodyTransform(b)
-					weapon.localTransform = TransformToLocalTransform(bt, t)
-					weapon.body = b
-					weapon.state = "idle"
-					weapon.idleTimer = 0
-					weapon.chargeTimer = 0
-					weapon.fireTimer = 0
-					weapon.fireCount = 0
-					weapons[i] = weapon
-				end
-			end
-		end
-
-		function getPerpendicular(dir)
-			local perp = VecNormalize(Vec(rnd(-1, 1), rnd(-1, 1), rnd(-1, 1)))
-			perp = VecNormalize(VecSub(perp, VecScale(dir, VecDot(dir, perp))))
-			return perp
-		end
-
-		function weaponFire(weapon, pos, dir)
-			local perp = getPerpendicular(dir)
-
-			-- This is the default bullet spread
-			local spread =  rnd(0.0, 1.0) / 9
-
-			-- Add more spread up based on aim, so that the first bullets never (well, rarely) hit player
-			local extraSpread = math.min(0.5, 2.0 / robot.distToPlayer)
-
-			dir = VecNormalize(VecAdd(dir, VecScale(perp, spread)))
-
-			--Start one voxel ahead to not hit robot itself
-			pos = VecAdd(pos, VecScale(dir, 0.1))
-
-			if weapon.type == "gun" then
-				PlaySound(shootSound, pos)
-				PointLight(pos, 1, 0.8, 0.6, 5)
-				Shoot(pos, dir, 0, weapon.strength)
-			elseif weapon.type == "rocket" then
-				PlaySound(rocketSound, pos)
-				Shoot(pos, dir, 1, weapon.strength)
-			end
-		end
-
-		function weaponsReset()
-			for i=1, #weapons do
-				weapons[i].state = "idle"
-				weapons[i].idleTimer = weapons[i].timeBetweenRounds
-				weapons[i].fire = 0
-			end
-		end
-
-		function weaponEmitFire(weapon, t, amount)
-			local p = TransformToParentPoint(t, Vec(0, 0, -0.1))
-			local d = TransformToParentVec(t, Vec(0, 0, -1))
-			ParticleReset()
-			ParticleTile(5)
-			ParticleColor(1, 1, 0.5, 1, 0, 0)
-			ParticleRadius(0.1*amount, 1*amount)
-			ParticleEmissive(10, 0)
-			ParticleDrag(0.1)
-			ParticleGravity(math.random()*20)
-			PointLight(p, 1, 0.8, 0.2, 2*amount)
-			PlayLoop(fireLoop, t.pos, amount)
-			SpawnParticle(p, VecScale(d, 12), 0.5 * amount)
-
-			if amount > 0.5 then
-				--Spawn fire
-				if not spawnFireTimer then
-					spawnFireTimer = 0
-				end
-				if spawnFireTimer > 0 then
-					spawnFireTimer = math.max(spawnFireTimer-0.01667, 0)
-				else
-					rejectAllBodies(robot.allBodies)
-					local hit, dist = QueryRaycast(p, d, 3)
-					if hit then
-						local wp = VecAdd(p, VecScale(d, dist))
-						SpawnFire(wp)
-						spawnFireTimer = 1
-					end
-				end
-
-				--Hurt player
-				local toPlayer = VecSub(GetPlayerCameraTransform().pos, t.pos)
-				local distToPlayer = VecLength(toPlayer)
-				local distScale = clamp(1.0 - distToPlayer / 5.0, 0.0, 1.0)
-				if distScale > 0 then
-					toPlayer = VecNormalize(toPlayer)
-					if VecDot(d, toPlayer) > 0.8 or distToPlayer < 0.5 then
-						rejectAllBodies(robot.allBodies)
-						local hit = QueryRaycast(p, toPlayer, distToPlayer)
-						if not hit or distToPlayer < 0.5 then
-							SetPlayerHealth(GetPlayerHealth() - 0.015 * weapon.strength * amount * distScale)
-						end
-					end
-				end
-			end
-		end
-
-		function weaponsUpdate(dt)
-			for i=1, #weapons do
-				local weapon = weapons[i]
-				local bt = GetBodyTransform(weapon.body)
-				local t = TransformToParentTransform(bt, weapon.localTransform)
-				local fwd = TransformToParentVec(t, Vec(0, 0, -2))
-				t.pos = VecAdd(t.pos, VecScale(fwd, 0.2))
-				local playerPos = VecCopy(robot.playerPos)
-				local toPlayer = VecSub(playerPos, t.pos)
-				local distToPlayer = VecLength(toPlayer)
-				toPlayer = VecNormalize(toPlayer)
-				local clearShot = false
-
-				if weapon.type == "fire" then
-					if not weapon.fire then
-						weapon.fire = 0
-						weaponStatus = "Idle"
-					end
-					if isShooting then
-						weapon.fire = math.min(weapon.fire + 0.1, 1.0)
-						weaponStatus = "Firing"
-					else
-						weapon.fire = math.max(weapon.fire - dt*0.5, 0.0)
-					end
-					if weapon.fire > 0 then
-						weaponEmitFire(weapon, t, weapon.fire)
-					else
-						weaponEmitFire(weapon, t, math.max(weapon.fire, 0.1))
-						weaponStatus = "Idle"
-					end
-				else
-					--Need to point towards player and have clear line of sight to have clear shot
-					local towardsPlayer = VecDot(fwd, toPlayer)
-					local gotAim = towardsPlayer > 0.9
-					-- if distToPlayer < 1.0 and towardsPlayer > 0.0 then
-					if isShooting then
-						gotAim = true
-					end
-					if isShooting then
-						QueryRequire("physical large")
-						rejectAllBodies(robot.allBodies)
-						local hit = QueryRaycast(t.pos, fwd, distToPlayer, 0, true)
-						if not hit then
-							clearShot =  true
-						end
-					end
-
-					--Handle states
-					if weapon.state == "idle" then
-						weaponStatus = "Idle"
-						weapon.idleTimer = weapon.idleTimer - dt
-						if weapon.idleTimer <= 0 and clearShot then
-							weapon.state = "charge"
-							weapon.fireDir = fwd
-							weapon.chargeTimer = weapon.chargeTime
-							weaponStatus = "Charging"
-						end
-					elseif weapon.state == "charge" or weapon.state == "chargesilent" then
-						weapon.chargeTimer = weapon.chargeTimer - dt
-						if weapon.state ~= "chargesilent" then
-							PlayLoop(chargeLoop, t.pos)
-						end
-						if weapon.chargeTimer <= 0 then
-							weapon.state = "fire"
-							weapon.fireTimer = 0
-							weapon.fireCount = weapon.shotsPerRound
-						end
-					elseif weapon.state == "fire" then
-						weapon.fireTimer = weapon.fireTimer - dt
-						if towardsPlayer > 0.3 or distToPlayer < 1.0 then
-							if weapon.fireTimer <= 0 then
-
-								weaponFire(weapon, t.pos, fwd)
-								weaponStatus = "Firing"
-
-								weapon.fireCount = weapon.fireCount - 1
-								if weapon.fireCount <= 0 then
-									if clearShot then
-										weapon.state = "chargesilent"
-										weapon.chargeTimer = weapon.chargeTime
-									else
-										weapon.state = "idle"
-										weapon.idleTimer = weapon.timeBetweenRounds
-									end
-								else
-									weapon.fireTimer = weapon.fireCooldown
-								end
-							end
-						else
-							--We are no longer pointing towards player, abort round
-							weapon.state = "idle"
-							weapon.idleTimer = weapon.timeBetweenRounds
-						end
-					end
-
-				end
-			end
-		end
-
-	end
-
-	--> Aims
-	do
-
-		aims = {}
-		aims_lights = {}
-
-		function aimsInit()
-			--! Added aims_lights
-			local lights = FindLights('weap_secondary')
-			local bodies = FindBodies("aim")
-			for i=1, #bodies do
-				local aim = {}
-				aim.body = bodies[i]
-				aims[i] = aim
-
-				for key, light in pairs(lights) do
-					local body = GetLightShape(light)
-					if body == aim.body then
-						aims_lights[i] = light
-					end
-				end
-
-			end
-		end
-
-		function aimsUpdate(dt)
-			for i=1, #aims do
-
-				local aim = aims[i]
-				local playerPos = getOuterCrosshairWorldPos()
-				local toPlayer = VecNormalize(VecSub(playerPos, GetBodyTransform(aim.body).pos))
-				local fwd = TransformToParentVec(GetBodyTransform(robot.body), Vec(0, 0, -1))
-
-				if (Eyes.canSeePlayer and VecDot(fwd, toPlayer) > 0.5) or robot.distToPlayer < 4.0 then
-					--Should aim
-					local v = 2
-					local f = 20
-					local wt = GetBodyTransform(aim.body)
-					local toPlayerOrientation = QuatLookAt(wt.pos, playerPos)
-					ConstrainOrientation(aim.body, robot.body, wt.rot, toPlayerOrientation, v, f)
-				else
-					--Should not aim
-					local rd = TransformToParentVec(GetBodyTransform(robot.body), Vec(0, 0, -1))
-					local wd = TransformToParentVec(GetBodyTransform(aim.body), Vec(0, 0, -1))
-					local angle = clamp(math.acos(VecDot(rd, wd)), 0, 1)
-					local v = 2
-					local f = math.abs(angle) * 10 + 3
-					ConstrainOrientation(robot.body, aim.body, GetBodyTransform(robot.body).rot, GetBodyTransform(aim.body).rot, v, f)
-				end
-
-			end
-		end
-
-	end
-
-	--> Sensor
-	do
-		sensor = {}
-		sensor.blocked = 0
-		sensor.blockedLeft = 0
-		sensor.blockedRight = 0
-		sensor.detectFall = 0
-
-		function sensorInit()
-		end
-
-		function sensorGetBlocked(dir, maxDist)
-			dir = VecNormalize(VecAdd(dir, rndVec(0.3)))
-			local origin = TransformToParentPoint(robot.transform, Vec(0, 0.8, 0))
-			QueryRequire("physical large")
-			rejectAllBodies(robot.allBodies)
-			local hit, dist = QueryRaycast(origin, dir, maxDist)
-			return 1.0 - dist/maxDist
-		end
-
-		function sensorDetectFall()
-			dir = Vec(0, -1, 0)
-			local lookAheadDist = 0.6 + clamp(VecLength(GetBodyVelocity(robot.body))/6.0, 0.0, 0.6)
-			local origin = TransformToParentPoint(robot.transform, Vec(0, 0.5, -lookAheadDist))
-			QueryRequire("physical large")
-			rejectAllBodies(robot.allBodies)
-			local maxDist = hover.distTarget + 1.0
-			local hit, dist = QueryRaycast(origin, dir, maxDist, 0.2)
-			return not hit
-		end
-
-		function sensorUpdate(dt)
-			local maxDist = config.sensorDist
-			local blocked = sensorGetBlocked(TransformToParentVec(robot.transform, Vec(0, 0, -1)), maxDist)
-			if sensorDetectFall() then
-				sensor.detectFall = 1.0
-			else
-				sensor.detectFall = 0.0
-			end
-			sensor.blocked = sensor.blocked * 0.9 + blocked * 0.1
-
-			local blockedLeft = sensorGetBlocked(TransformToParentVec(robot.transform, Vec(-0.5, 0, -1)), maxDist)
-			sensor.blockedLeft = sensor.blockedLeft * 0.9 + blockedLeft * 0.1
-
-			local blockedRight = sensorGetBlocked(TransformToParentVec(robot.transform, Vec(0.5, 0, -1)), maxDist)
-			sensor.blockedRight = sensor.blockedRight * 0.9 + blockedRight * 0.1
-		end
-
-	end
-
-	--> Hearing
-	do
-
-		hearing = {}
-		hearing.lastSoundPos = Vec(0, -100, 0)
-		hearing.lastSoundVolume = 0
-		hearing.timeSinceLastSound = 0
-		hearing.hasNewSound = false
-
-		function hearingInit()
-		end
-
-		function hearingUpdate(dt)
-			hearing.timeSinceLastSound = hearing.timeSinceLastSound + dt
-			if config.canHearPlayer then
-				local vol, pos = GetLastSound()
-				local dist = VecDist(robot.transform.pos, pos)
-				if vol > 0.1 and dist > 4.0 and dist < config.maxSoundDist then
-					local valid = true
-					--If there is an investigation trigger, the robot is in it and the sound is not, ignore sound
-					if robot.investigateTrigger ~= 0 and IsPointInTrigger(robot.investigateTrigger, robot.bodyCenter) and not IsPointInTrigger(robot.investigateTrigger, pos) then
-						valid = false
-					end
-					--React if time has passed since last sound or if it's substantially stronger
-					if valid and (hearing.timeSinceLastSound > 2.0 or vol > hearing.lastSoundVolume*2.0) then
-						local attenuation = 5.0 / math.max(5.0, dist)
-						attenuation = attenuation * attenuation
-						local heardVolume = vol * attenuation
-						if heardVolume > 0.05 then
-							hearing.lastSoundVolume = vol
-							hearing.lastSoundPos = pos
-							hearing.timeSinceLastSound = 0
-							hearing.hasNewSound = true
-						end
-					end
-				end
-			end
-		end
-
-		function hearingConsumeSound()
-			hearing.hasNewSound = false
-		end
-
-	end
-end
-
-
-
---= OTHER
-do
-	--> Util
-	do
-
-		function truncateToGround(pos)
-			rejectAllBodies(robot.allBodies)
-			QueryRejectVehicle(GetPlayerVehicle())
-			hit, dist = QueryRaycast(pos, Vec(0, -1, 0), 5, 0.2)
-			if hit then
-				pos = VecAdd(pos, Vec(0, -dist, 0))
-			end
-			return pos
-		end
-
-		function getRandomPosInTrigger(trigger)
-			local mi, ma = GetTriggerBounds(trigger)
-			local minDist = math.max(ma[1]-mi[1], ma[3]-mi[3])*0.25
-			minDist = math.min(minDist, 5.0)
-
-			for i=1, 100 do
-				local probe = Vec()
-				for j=1, 3 do
-					probe[j] = mi[j] + (ma[j]-mi[j])*rnd(0,1)
-				end
-				if IsPointInTrigger(trigger, probe) then
-					return probe
-				end
-			end
-			return VecLerp(mi, ma, 0.5)
-		end
-
-		function handleCommand(cmd)
-			words = splitString(cmd, " ")
-			if #words == 5 then
-				if words[1] == "explosion" then
-					local strength = tonumber(words[2])
-					local x = tonumber(words[3])
-					local y = tonumber(words[4])
-					local z = tonumber(words[5])
-					hitByExplosion(strength/2, Vec(x,y,z))
-				end
-			end
-			if #words == 8 then
-				if words[1] == "shot" then
-					local strength = tonumber(words[2])
-					local x = tonumber(words[3])
-					local y = tonumber(words[4])
-					local z = tonumber(words[5])
-					local dx = tonumber(words[6])
-					local dy = tonumber(words[7])
-					local dz = tonumber(words[8])
-					hitByShot(strength/1.5, Vec(x,y,z), Vec(dx,dy,dz))
-				end
-			end
-		end
-
-
-		function getClosestPatrolIndex()
-			local bestIndex = 1
-			local bestDistance = 999
-			for i=1, #patrolLocations do
-				local pt = GetLocationTransform(patrolLocations[i]).pos
-				local d = VecLength(VecSub(pt, robot.transform.pos))
-				if d < bestDistance then
-					bestDistance = d
-					bestIndex = i
-				end
-			end
-			return bestIndex
-		end
-
-
-		function getDistantPatrolIndex(currentPos)
-			local bestIndex = 1
-			local bestDistance = 0
-			for i=1, #patrolLocations do
-				local pt = GetLocationTransform(patrolLocations[i]).pos
-				local d = VecLength(VecSub(pt, currentPos))
-				if d > bestDistance then
-					bestDistance = d
-					bestIndex = i
-				end
-			end
-			return bestIndex
-		end
-
-
-		function getNextPatrolIndex(current)
-			local i = current + 1
-			if i > #patrolLocations then
-				i = 1
-			end
-			return i
-		end
-
-
-		function markPatrolLocationAsActive(index)
-			for i=1, #patrolLocations do
-				if i==index then
-					SetTag(patrolLocations[i], "active")
-				else
-					RemoveTag(patrolLocations[i], "active")
-				end
-			end
-		end
-
-
-		function debugState()
-			local state = stackTop()
-			DebugWatch("state", state.id)
-			DebugWatch("activeTime", state.activeTime)
-			DebugWatch("totalTime", state.totalTime)
-			DebugWatch("navigation.state", navigation.state)
-			DebugWatch("#navigation.path", #navigation.path)
-			DebugWatch("navigation.hasNewTarget", navigation.hasNewTarget)
-			DebugWatch("robot.blocked", robot.blocked)
-			DebugWatch("robot.speed", robot.speed)
-			DebugWatch("navigation.blocked", navigation.blocked)
-			DebugWatch("navigation.unblock", navigation.unblock)
-			DebugWatch("navigation.unblockTimer", navigation.unblockTimer)
-			DebugWatch("navigation.thinkTime", navigation.thinkTime)
-			DebugWatch("GetPathState()", GetPathState())
-		end
-
-
-		function canBeSeenByPlayer()
-			for i=1, #robot.allShapes do
-				if IsShapeVisible(robot.allShapes[i], config.outline, true) then
-					return true
-				end
-			end
-			return false
-		end
-
-		function hitByExplosion(strength, pos)
-			--Explosions smaller than 1.0 are ignored (with a bit of room for rounding errors)
-			if strength > 0.99 then
-				local d = VecDist(pos, robot.bodyCenter)
-				local f = clamp((1.0 - d/10.0), 0.0, 1.0) * strength
-				if f > 0.2 then
-					robot.stunned = robot.stunned + f * 4.0
-				end
-
-				--Give robots an extra push if they are not already moving that much
-				--Unphysical but more fun
-				local maxVel = 7.0
-				local strength = 3.0
-				local dir = VecNormalize(VecSub(robot.bodyCenter, pos))
-				--Tilt direction slightly upwards to make them fly more
-				dir[2] = dir[2] + 0.2
-				dir = VecNormalize(dir)
-				for i=1, #robot.allBodies do
-					local b = robot.allBodies[i]
-					local v = GetBodyVelocity(b)
-					local scale = clamp(1.0-VecLength(v)/maxVel, 0.0, 1.0)
-					local velAdd = math.min(maxVel, f*scale*strength)
-					if velAdd > 0 then
-						v = VecAdd(v, VecScale(dir, velAdd))
-						SetBodyVelocity(b, v)
-					end
-				end
-			end
-		end
-
-
-		function hitByShot(strength, pos, dir)
-			if VecDist(pos, robot.bodyCenter) < 3 then
-				local hit, point, n, shape = QueryClosestPoint(pos, 0.1)
-				if hit then
-					for i=1, #robot.allShapes do
-						if robot.allShapes[i] == shape then
-							robot.stunned = robot.stunned + 0.2
-							return
-						end
-					end
-				end
-			end
-		end
-
-	end
-
-	--> Physics
-	do
-
-		function VecDist(a, b)
-			return VecLength(VecSub(a, b))
-		end
-
-		function rndVec(length)
-			local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
-			return VecScale(v, length)
-		end
-
-		function rnd(mi, ma)
-			local v = math.random(0,1000) / 1000
-			return mi + (ma-mi)*v
-		end
-
-		function rejectAllBodies(bodies)
-			for i=1, #bodies do
-				QueryRejectBody(bodies[i])
-			end
-		end
-
-		function getTagParameter(entity, name, default)
-			local v = tonumber(GetTagValue(entity, name))
-			if v then
-				return v
-			else
-				return default
-			end
-		end
-
-		function getTagParameter2(entity, name, default)
-			local s = splitString(GetTagValue(entity, name), ",")
-			if #s == 1 then
-				local v = tonumber(s[1])
-				if v then
-					return v, v
-				else
-					return default, default
-				end
-			elseif #s == 2 then
-				local v1 = tonumber(s[1])
-				local v2 = tonumber(s[2])
-				if v1 and v2 then
-					return v1, v2
-				else
-					return default, default
-				end
-			else
-				return default, default
-			end
-		end
-
-	end
-
-	--> Logic
-	do
-		stack = {}
-		stack.list = {}
-
-		function stackTop()
-			return stack.list[#stack.list]
-		end
-
-		function stackPush(id)
-			local index = #stack.list+1
-			stack.list[index] = {}
-			stack.list[index].id = id
-			stack.list[index].totalTime = 0
-			stack.list[index].activeTime = 0
-			return stack.list[index]
-		end
-
-		function stackPop(id)
-			if id then
-				while stackHas(id) do
-					stackPop()
-				end
-			else
-				if #stack.list > 1 then
-					stack.list[#stack.list] = nil
-				end
-			end
-		end
-
-		function stackHas(s)
-			return stackGet(s) ~= nil
-		end
-
-		function stackGet(id)
-			for i=1,#stack.list do
-				if stack.list[i].id == id then
-					return stack.list[i]
-				end
-			end
-			return nil
-		end
-
-		function stackClear(s)
-			stack.list = {}
-			stackPush("none")
-		end
-
-		function stackInit()
-			stackClear()
-		end
-
-		function stackUpdate(dt)
-			if #stack.list > 0 then
-				for i=1, #stack.list do
-					stack.list[i].totalTime = stack.list[i].totalTime + dt
-				end
-
-				--Tick total time
-				stack.list[#stack.list].activeTime = stack.list[#stack.list].activeTime + dt
-			end
-		end
-	end
-end
+#version 2

```

---

# Migration Report: custom_robot\scripts\robot_default_custom.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_robot\scripts\robot_default_custom.lua
+++ patched/custom_robot\scripts\robot_default_custom.lua
@@ -1,11 +1,4 @@
---================================================================
---= Robot Vehicles
---= By: Cheejins
---================================================================
---= This script is only used for the built in robots.
---================================================================
-
---> SCRIPT
+#version 2
 function initCustom()
 
 	CAMERA = {}
@@ -37,6 +30,7 @@
 	end
 
 end
+
 function tickCustom(dt)
 
 	--+ Global robot variables.
@@ -64,6 +58,7 @@
 	end
 
 end
+
 function updateCustom(dt)
 	robot.speedScale = regGetFloat('robot.move.speed')
 	timers.gun.bullets.rpm = regGetFloat('robot.weapon.bullet.rpm')
@@ -75,12 +70,13 @@
 
 	-- elseif regGetBool('robot.followPlayer') then
 
-	-- 	if VecDist(GetPlayerTransform().pos, robot.transform.pos) > 3 then
+	-- 	if VecDist(GetPlayerTransform(playerId).pos, robot.transform.pos) > 3 then
 	-- 		robotFollowPlayer(dt)
 	-- 	end
 
 	end
 end
+
 function drawCustom()
 
 	if player.isDrivingRobot and robot.enabled then
@@ -117,8 +113,6 @@
 
 		UiPop() end
 
-
-
 		uiManageGameOptions()
 
 		CAMERA.xy = {UiCenter(), UiMiddle()}
@@ -142,7 +136,6 @@
 			UiColor(1,1,1, 1)
 			UiImageBox("ui/hud/location-dot.png", 6, 6, 0,0)
 
-
 		UiPop() end
 
 		-- Bottom info
@@ -170,7 +163,7 @@
 				if InputPressed('any') then
 					enterCount = enterCount + 1
 					if enterCount > 1 then
-						SetBool('LEVEL.welcome', true)
+						SetBool('LEVEL.welcome', true, true)
 					end
 				end
 
@@ -181,84 +174,12 @@
 
 end
 
-
-
---> MOVEMENT
-processMovement = function ()
-
-	-- navigationClear()
-
-	local walk = false
-	local walkDir = Vec()
-	local lookTr = Transform(robot.transform.pos, camTr.rot)
-
-	--+ WASD
-	if InputDown('up') then
-		local moveDir = TransformToParentVec(lookTr, Vec(0,0,-1))
-		walkDir = VecAdd(walkDir, moveDir)
-		walk = true
-	elseif InputDown('down') then
-		local moveDir = TransformToParentVec(lookTr, Vec(0,0,1))
-		walkDir = VecAdd(walkDir, moveDir)
-		walk = true
-	end
-
-	if InputDown('left') then
-		local moveDir = TransformToParentVec(lookTr, Vec(-1,0,0))
-		walkDir = VecAdd(walkDir, moveDir)
-		walk = true
-	end
-	if InputDown('right') then
-		local moveDir = TransformToParentVec(lookTr, Vec(1,0,0))
-		walkDir = VecAdd(walkDir, moveDir)
-		walk = true
-	end
-
-	if walk then
-		walkDir = VecNormalize(walkDir)
-		robotWalk(walkDir)
-	end
-
-	--+ Sprint
-	if InputDown('shift') then
-		robot.speedScale = regGetFloat('robot.move.speed') * 2
-	else
-		robot.speedScale = regGetFloat('robot.move.speed')
-	end
-
-	--+ Jump
-	if InputPressed('space') then
-		SetBodyVelocity(robot.body, VecAdd(GetBodyVelocity(robot.body), Vec(0,10,0)))
-	end
-
-	--+ Crouch
-	if InputPressed('ctrl') then
-		SetBodyVelocity(robot.body, VecAdd(GetBodyVelocity(robot.body), Vec(0,-5,0)))
-		-- DebugPrint('Teabag initiated ' .. sfnTime())
-	end
-
-end
-robotWalk = function (robotDir)
-	robot.dir = robotDir
-	local dirDiff = VecDot(VecScale(robot.axes[3], -1), robot.dir)
-	local speedScale = math.max(0.25, dirDiff)
-	speedScale = speedScale * clamp(1.0 - navigation.vertical, 0.3, 1.0)
-	robot.speed = config.speed * speedScale
-end
-robotFollowPlayer = function(dt)
-	navigationSetTarget(GetPlayerTransform().pos, 5)
-	navigationMove(dt)
-	navigationUpdate(dt)
-end
-
-
-
---> WEAPONS
 function processWeapons()
 
 	isShooting = InputDown('lmb')
 
 end
+
 function processWeapons_mech_aeon()
 
 	-- Draw dots at shooting positions.
@@ -270,6 +191,7 @@
 	-- end
 
 end
+
 function aimsUpdateCustom()
 	for i=1, #aims do
 		local aim = aims[i]
@@ -293,20 +215,14 @@
 	end
 end
 
-
-
---> PLAYER
-player = {}
-player.isDrivingRobot = false
 function playerDriveRobot(dt, pos)
 
 	--+ Update player values.
-	SetPlayerTransform(Transform(pos))
-	SetPlayerHealth(1)
-	SetString("game.player.tool", 'sledge')
-	SetPlayerVelocity(Vec())
+	SetPlayerTransform(playerId, Transform(pos))
+	SetPlayerHealth(playerId, 1)
+	SetString("game.player.tool", 'sledge', true)
+	SetPlayerVelocity(playerId, Vec())
 	SetPlayerGroundVelocity(Vec())
-
 
 	manageCamera(UI_OPTIONS, robot.cameraHeight)
 
@@ -325,6 +241,7 @@
 	end
 
 end
+
 function playerCheckRobot()
 
 	if robot.enabled then
@@ -335,13 +252,13 @@
 			if InputPressed('interact') or InputPressed('e') then
 				player.isDrivingRobot = false
 				local playerExitTr = Transform(TransformToParentPoint(bodyTr, Vec(0,0,-2)))
-				SetPlayerTransform(playerExitTr)
+				SetPlayerTransform(playerId, playerExitTr)
 			end
 
 		elseif InputPressed('interact') or InputPressed('e') then
 
 			--+ Enter robot.
-			if GetPlayerInteractBody() == Eyes.body then
+			if GetPlayerInteractBody(playerId) == Eyes.body then
 				player.isDrivingRobot = true
 			end
 
@@ -355,18 +272,16 @@
 	else
 
 		player.isDrivingRobot = false
-		SetBool('level.playerIsDrivingRobot', false)
-
-	end
-
-end
-
-
-
---> OTHER
+		SetBool('level.playerIsDrivingRobot', false, true)
+
+	end
+
+end
+
 function debugRobot()
 	dbw('model', robot.model)
 end
+
 function setRobotUnbreakable(setUnbreakable)
 
 	local func_setter
@@ -393,18 +308,20 @@
 	end
 
 end
+
 function initPlayerDrivingRobot()
 
 	-- if GetBool('level.robotExists') then
 
 	-- 	if not GetBool('level.playerIsDrivingRobot') then
 	-- 		-- player.isDrivingRobot = true
-	-- 		SetBool('level.playerIsDrivingRobot', true)
+	-- 		SetBool('level.playerIsDrivingRobot', true, true)
 	-- 	end
 
 	-- end
 
 end
+
 function manageRobotHealth()
 
 	-- if robot.enabled and getRobotMass() < robot.health*0.9 then
@@ -438,6 +355,7 @@
 	-- end
 
 end
+
 function getRobotMass()
 	local mass = 0
 	for key, body in pairs(robot.allBodies) do
@@ -446,3 +364,4 @@
 	end
 	return mass
 end
+

```

---

# Migration Report: custom_robot\scripts\robotPreset.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_robot\scripts\robotPreset.lua
+++ patched/custom_robot\scripts\robotPreset.lua
@@ -1,9 +1,4 @@
-robot_models = {
-    aeon = 'aeon',
-    basic = 'basic',
-}
-
-
+#version 2
 function initRobotPreset()
 
     local robot_model = GetTagValue(robot.body, 'model')
@@ -11,7 +6,6 @@
     setRobotCrosshairScale()
 
 end
-
 
 function createRobotObject(robot_model)
 
@@ -25,20 +19,17 @@
 
 end
 
-
 function setWeaponLocations(robot)
 
     local lights_weap_primary = FindLights('weap_primary')
     local lights_weap_secondary = FindLights('weap_secondary')
     local lights_weap_special = FindLights('weap_special')
 
-
     local weaponObjects = {
         primary = {},
         secondary = {},
         special = {},
     }
-
 
     for key, light in pairs(lights_weap_primary) do
 
@@ -67,12 +58,10 @@
 
     end
 
-
     robot.weaponObjects = weaponObjects
 
 end
 
---- Returns the light, its shape and body.
 function getLightObject(light)
 
     local l = {}
@@ -87,7 +76,6 @@
 
 end
 
-
 function setRobotCrosshairScale()
 
     if robot.model == robot_models.aeon then
@@ -96,4 +84,5 @@
         robot.crosshairScale = 1
     end
 
-end+end
+

```

---

# Migration Report: custom_robot\scripts\sounds.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_robot\scripts\sounds.lua
+++ patched/custom_robot\scripts\sounds.lua
@@ -1,3 +1,4 @@
+#version 2
 function initSounds()
     Sounds = {
 
@@ -37,8 +38,8 @@
     }
 end
 
-
 function PlayRandomSound(soundTable, pos, vol, index_override)
     local p = index_override or soundTable[math.random(1, #soundTable)]
     PlaySound(p, pos, vol or 1)
 end
+

```

---

# Migration Report: custom_robot\scripts\timers.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_robot\scripts\timers.lua
+++ patched/custom_robot\scripts\timers.lua
@@ -1,4 +1,4 @@
--- Timers that count down constantly.
+#version 2
 function runTimers()
     TimerRunTime(timers.gun.bullets)
     TimerRunTime(timers.gun.rockets)
@@ -24,3 +24,4 @@
     }
 
 end
+

```

---

# Migration Report: custom_robot\scripts\ui.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_robot\scripts\ui.lua
+++ patched/custom_robot\scripts\ui.lua
@@ -1,7 +1,4 @@
-------------------------------------------------------------------------------------------------
--- Please don't judge this code too heavily. It is a bit of a hack job but it works :)
-------------------------------------------------------------------------------------------------
-
+#version 2
 function initUi()
     UI_OPTIONS = false
 
@@ -24,7 +21,6 @@
 
         marginYSize = 50
         local marginY = 0
-
 
         UiTranslate(UiCenter()/1.35, 50)
 
@@ -63,22 +59,22 @@
 
                 UiImageBox("ui/common/box-outline-fill-6.png", 150, 50, 10, 10)
                 if UiTextButton('Balanced') then
-                    regSetFloat('robot.weapon.bullet.rpm', 800)
-                    regSetFloat('robot.weapon.bullet.holeSize', 0.5)
+                    regSetFloat('robot.weapon.bullet.rpm', 800, true)
+                    regSetFloat('robot.weapon.bullet.holeSize', 0.5, true)
                 end
                 UiTranslate(0, 64)
 
                 UiImageBox("ui/common/box-outline-fill-6.png", 150, 50, 10, 10)
                 if UiTextButton('Shredder') then
-                    regSetFloat('robot.weapon.bullet.rpm', 2400)
-                    regSetFloat('robot.weapon.bullet.holeSize', 0.75)
+                    regSetFloat('robot.weapon.bullet.rpm', 2400, true)
+                    regSetFloat('robot.weapon.bullet.holeSize', 0.75, true)
                 end
                 UiTranslate(0, 64)
 
                 UiImageBox("ui/common/box-outline-fill-6.png", 150, 50, 10, 10)
                 if UiTextButton('Dissolver') then
-                    regSetFloat('robot.weapon.bullet.rpm', 400)
-                    regSetFloat('robot.weapon.bullet.holeSize', 4)
+                    regSetFloat('robot.weapon.bullet.rpm', 400, true)
+                    regSetFloat('robot.weapon.bullet.holeSize', 4, true)
                 end
                 UiTranslate(0, 64)
 
@@ -89,7 +85,6 @@
             end
 
         UiPop() end
-
 
         do UiPush()
 
@@ -114,14 +109,12 @@
                 modReset()
             end
 
-
         UiPop() end
 
     UiPop() end
 
 end
 
---- Manage when to open and close the options menu.
 function uiManageGameOptions()
 
     if player.isDrivingRobot and robot.model == robot_models.basic then
@@ -136,3 +129,4 @@
     end
 
 end
+

```

---

# Migration Report: custom_robot\scripts\ui_components.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_robot\scripts\ui_components.lua
+++ patched/custom_robot\scripts\ui_components.lua
@@ -1,17 +1,4 @@
-ui = {}
-
-ui.colors = {
-    white = Vec(1,1,1),
-    g3 = Vec(0.5,0.5,0.5),
-    g2 = Vec(0.35,0.35,0.35),
-    g1 = Vec(0.2,0.2,0.2),
-    black = Vec(0,0,0),
-}
-
-
-
-ui.slider = {}
-
+#version 2
 function ui.slider.create(title, registryPath, valueText, min, max, w, h, fontSize, axis)
 
     local value = GetFloat('savegame.mod.' .. registryPath)
@@ -41,7 +28,7 @@
     value, done = UiSlider("ui/common/dot.png", "x", value, 0, slW)
     if done then
         local val = (value/slW) * (max-min) + min -- Convert to true scale.
-        SetFloat('savegame.mod.' .. registryPath, val)
+        SetFloat('savegame.mod.' .. registryPath, val, true)
     end
 
     -- Slider value
@@ -53,9 +40,6 @@
     UiPop() end
 
 end
-
-
-ui.checkBox = {}
 
 function ui.checkBox.create(title, registryPath)
 
@@ -103,8 +87,9 @@
 
     UiButtonImageBox('ui/common/box-outline-6.png', 10,10, 0,0,0, a)
     if UiBlankButton(tglW, tglH) then
-        SetBool('savegame.mod.' .. registryPath, not value)
+        SetBool('savegame.mod.' .. registryPath, not value, true)
         PlaySound(LoadSound('clickdown.ogg'), GetCameraTransform().pos, 1)
     end
 
-end+end
+

```

---

# Migration Report: custom_robot\scripts\umf.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_robot\scripts\umf.lua
+++ patched/custom_robot\scripts\umf.lua
@@ -1,4585 +1,3 @@
-local __RUNLATER = {} UMF_RUNLATER = function(code) __RUNLATER[#__RUNLATER + 1] = code end
---src/core/hook.lua
-(function() 
+#version 2
+local __RUNLATER = {}
 
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
- end)();
---src/util/detouring.lua
-(function() 
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
-	original[name] = _G[name]
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
- end)();
---src/core/hooks_base.lua
-(function() 
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
- end)();
---src/core/hooks_extra.lua
-(function() 
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
- end)();
---src/util/registry.lua
-(function() 
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
---- Creates a channel shared via the registry.
----
----@param name string Name of the channel.
----@param max? number Maximum amount of unread messages in the channel.
----@param local_realm? string Name to use to identify the local recipient.
----@return table
-function util.shared_channel( name, max, local_realm )
-	max = max or 64
-	local channel = {
-		_buffer = util.shared_buffer( name, max ),
-		_offset = 0,
-		_hooks = {},
-		_ready_count = 0,
-		_ready = {},
-		broadcast = function( self, ... )
-			return self:send( "", ... )
-		end,
-		send = function( self, realm, ... )
-			self._buffer:push( string.format( ",%s,;%s",
-			                                  (type( realm ) == "table" and table.concat( realm, "," ) or tostring( realm )),
-			                                  util.serialize( ... ) ) )
-		end,
-		listen = function( self, callback )
-			if self._ready[callback] ~= nil then
-				return
-			end
-			self._hooks[#self._hooks + 1] = callback
-			self:ready( callback )
-			return callback
-		end,
-		unlisten = function( self, callback )
-			self:unready( callback )
-			self._ready[callback] = nil
-			for i = 1, #self._hooks do
-				if self._hooks[i] == callback then
-					table.remove( self._hooks, i )
-					return true
-				end
-			end
-		end,
-		ready = function( self, callback )
-			if not self._ready[callback] then
-				self._ready_count = self._ready_count + 1
-				self._ready[callback] = true
-			end
-		end,
-		unready = function( self, callback )
-			if self._ready[callback] then
-				self._ready_count = self._ready_count - 1
-				self._ready[callback] = false
-			end
-		end,
-	}
-	local_realm = "," .. (local_realm or "unknown") .. ","
-	local function receive( ... )
-		for i = 1, #channel._hooks do
-			local f = channel._hooks[i]
-			if channel._ready[f] then
-				f( channel, ... )
-			end
-		end
-	end
-	hook.add( "base.tick", name, function( dt )
-		if channel._ready_count > 0 then
-			local last_pos = channel._buffer:pos()
-			if last_pos > channel._offset then
-				for i = math.max( channel._offset, last_pos - max ), last_pos - 1 do
-					local message = channel._buffer:get_g( i )
-					local start = message:find( ";", 1, true )
-					local realms = message:sub( 1, start - 1 )
-					if realms == ",," or realms:find( local_realm, 1, true ) then
-						receive( util.unserialize( message:sub( start + 1 ) ) )
-						if channel._ready_count <= 0 then
-							channel._offset = i + 1
-							return
-						end
-					end
-				end
-				channel._offset = last_pos
-			end
-		end
-	end )
-	return channel
-end
-
---- Creates an async reader on a channel for coroutines.
----
----@param channel table Name of the channel.
----@return table
-function util.async_channel( channel )
-	local listener = {
-		_channel = channel,
-		_waiter = nil,
-		read = function( self )
-			self._waiter = coroutine.running()
-			if not self._waiter then
-				error( "async_channel:read() can only be used in a coroutine" )
-			end
-			self._channel:ready( self._handler )
-			return coroutine.yield()
-		end,
-		close = function( self )
-			if self._handler then
-				self._channel:unlisten( self._handler )
-			end
-		end,
-	}
-	listener._handler = listener._channel:listen( function( _, ... )
-		if listener._waiter then
-			local co = listener._waiter
-			listener._waiter = nil
-			listener._channel:unready( listener._handler )
-			return coroutine.resume( co, ... )
-		end
-	end )
-	listener._channel:unready( listener._handler )
-	return listener
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
-	hook.add( "api.newmeta", "api.createunserializer", function( name, meta )
-		gets[name] = function( key )
-			return setmetatable( {}, meta ):__unserialize( GetString( key ) )
-		end
-		sets[name] = function( key, value )
-			return SetString( key, meta.__serialize( value ) )
-		end
-	end )
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
-					root[k] = util.structured_table( key, v )
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
-						return gets[entry.type]( entry.key )
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
- end)();
---src/util/debug.lua
-(function() 
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
- end)();
---src/core/console_backend.lua
-(function() 
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
- end)();
---src/core/_index.lua
-(function() 
-
-GLOBAL_CHANNEL = util.shared_channel( "game.umf_global_channel", 128 )
- end)();
---src/util/meta.lua
-(function() 
-
-local registered_meta = {}
-local reverse_meta = {}
-
---- Defines a new metatable type.
----
----@param name string
----@param parent? string
----@return table
-function global_metatable( name, parent )
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
-		hook.saferun( "api.newmeta", name, meta )
-	end
-	if parent then
-		setmetatable( meta, global_metatable( parent ) )
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
--- I hate this but without a pre-quicksave handler I see no other choice.
-local previous = -2
-hook.add( "base.tick", "api.metatables.save", function( ... )
-	if GetTime() - previous > 2 then
-		previous = GetTime()
-		_G.GLOBAL_META_SAVE = findmeta( _G, {} )
-	end
-end )
-
-local function restoremeta( dst, src )
-	for k, v in pairs( src ) do
-		local dv = dst[k]
-		if type( dv ) == "table" then
-			if v[1] then
-				setmetatable( dv, global_metatable( v[1] ) )
-			end
-			if v[2] then
-				restoremeta( dv, v[2] )
-			end
-		end
-	end
-end
-
-hook.add( "base.command.quickload", "api.metatables.restore", function( ... )
-	if GLOBAL_META_SAVE then
-		restoremeta( _G, GLOBAL_META_SAVE )
-	end
-end )
- end)();
---src/util/timer.lua
-(function() 
-
-----------------------------------------
---              WARNING               --
---   Timers are reset on quickload!   --
--- Keep this in mind if you use them. --
-----------------------------------------
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
- end)();
---src/util/visual.lua
-(function() 
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
-		local points = {}
-		local iteration = 1
-		local pow, sqrt, sin, cos = math.pow, math.sqrt, math.sin, math.cos
-		local r, g, b, a
-		local DrawFunction = DrawLine
-
-		radius = sqrt( 2 * pow( radius, 2 ) ) or sqrt( 2 )
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
-			points[iteration] = TransformToParentPoint( transform, Vec( sin( (v + rotation) * degreeToRadian ) * radius, 0,
-			                                                            cos( (v + rotation) * degreeToRadian ) * radius ) )
-			points[iteration + 1] = TransformToParentPoint( transform,
-			                                                Vec( sin( ((v + 360 / sides) + rotation) * degreeToRadian ) * radius,
-			                                                     0,
-			                                                     cos( ((v + 360 / sides) + rotation) * degreeToRadian ) * radius ) )
-			if iteration > 2 then
-				DrawFunction( points[iteration], points[iteration + 1], r, g, b, a )
-			end
-			iteration = iteration + 2
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
-end
- end)();
---src/util/xml.lua
-(function() 
----@class XMLNode
----@field __call fun(children: XMLNode[]): XMLNode
----@field attributes table<string, string> | nil
----@field children XMLNode[] | nil
----@field type string
-local xmlnode = {
-	--- Renders this node into an XML string.
-	---
-	---@return string
-	Render = function( self )
-		local attr = ""
-		if self.attributes then
-			for name, val in pairs( self.attributes ) do
-				attr = string.format( "%s %s=%q", attr, name, val )
-			end
-		end
-		local children = {}
-		if self.children then
-			for i = 1, #self.children do
-				children[i] = self.children[i]:Render()
-			end
-		end
-		return string.format( "<%s%s>%s</%s>", self.type, attr, table.concat( children, "" ), self.type )
-	end,
-}
-
-local meta = {
-	__call = function( self, children )
-		self.children = children
-		return self
-	end,
-	__index = xmlnode,
-}
-
---- Defines an XML node.
----
----@param type string
----@return fun(attributes: table<string, string>): XMLNode
-XMLTag = function( type )
-	return function( attributes )
-		return setmetatable( { type = type, attributes = attributes }, meta )
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
- end)();
---src/vector/quat.lua
-(function() 
-
----@type Vector
-local vector_meta = global_metatable( "vector" )
----@class Quaternion
-local quat_meta = global_metatable( "quaternion" )
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
-	self[1] = self[1] / o
-	self[2] = self[2] / o
-	self[3] = self[3] / o
-	self[4] = self[4] / o
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
- end)();
---src/vector/transform.lua
-(function() 
-
----@type Vector
-local vector_meta = global_metatable( "vector" )
----@type Quaternion
-local quat_meta = global_metatable( "quaternion" )
----@class Transformation
----@field pos Vector
----@field rot Quaternion
-local transform_meta = global_metatable( "transformation" )
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
- end)();
---src/vector/vector.lua
-(function() 
-
----@class Vector
-local vector_meta = global_metatable( "vector" )
----@type Quaternion
-local quat_meta = global_metatable( "quaternion" )
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
- end)();
---src/entities/entity.lua
-(function() 
-
----@class Entity
----@field handle number
----@field type string
-local entity_meta = global_metatable( "entity" )
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
- end)();
---src/entities/body.lua
-(function() 
-
----@class Body: Entity
-local body_meta = global_metatable( "body", "entity" )
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
- end)();
---src/entities/joint.lua
-(function() 
-
----@class Joint: Entity
-local joint_meta = global_metatable( "joint", "entity" )
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
----@return string
-function joint_meta:__tostring()
-	return string.format( "Joint[%d]", self.handle )
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
- end)();
---src/entities/light.lua
-(function() 
-
----@class Light: Entity
-local light_meta = global_metatable( "light", "entity" )
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
- end)();
---src/entities/location.lua
-(function() 
-
----@class Location: Entity
-local location_meta = global_metatable( "location", "entity" )
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
- end)();
---src/entities/player.lua
-(function() 
-
----@class Player
-local player_meta = global_metatable( "player" )
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
- end)();
---src/entities/screen.lua
-(function() 
-
----@class Screen: Entity
-local screen_meta = global_metatable( "screen", "entity" )
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
- end)();
---src/entities/shape.lua
-(function() 
-
----@class Shape: Entity
-local shape_meta = global_metatable( "shape", "entity" )
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
- end)();
---src/entities/trigger.lua
-(function() 
-
----@class Trigger: Entity
-local trigger_meta = global_metatable( "trigger", "entity" )
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
- end)();
---src/entities/vehicle.lua
-(function() 
-
----@class Vehicle: Entity
-local vehicle_meta = global_metatable( "vehicle", "entity" )
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
- end)();
---src/animation/animation.lua
-(function() 
-
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
- end)();
---src/animation/armature.lua
-(function() 
-
----@class Armature
----@field refs any
----@field root any
----@field scale number | nil
----@field dirty boolean
-local armature_meta = global_metatable( "armature" )
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
---- Loads armature information from a prefab and a list of shapes.
----
----@param xml string
----@param parts table[]
----@param scale? number
-function LoadArmatureFromXML( xml, parts, scale ) -- Example below
-	scale = scale or 1
-	local dt = ParseXML( xml )
-	assert( dt.type == "prefab" and dt.children[1] and dt.children[1].type == "group" )
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
-	local bones = translatebone( dt.children[1] )[1]
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
-    <group id_="1196432640" open_="true" name="instance=MOD/physgun.xml" pos="-3.4 0.7 0.0" rot="0.0 0.0 0.0">
-        <vox id_="1866644736" pos="-0.125 -0.125 0.125" file="MOD/physgun.vox" object="body" scale="0.5"/>
-        <group id_="279659168" open_="true" name="core0" pos="0.0 0.0 -0.075" rot="0.0 0.0 0.0">
-            <vox id_="496006720" pos="-0.025 -0.125 0.0" rot="0.0 0.0 0.0" file="MOD/physgun.vox" object="core_0" scale="0.5"/>
-        </group>
-        <group id_="961930560" open_="true" name="core1" pos="0.0 0.0 -0.175" rot="0.0 0.0 0.0">
-            <vox id_="1109395584" pos="-0.025 -0.125 0.0" rot="0.0 0.0 0.0" file="MOD/physgun.vox" object="core_1" scale="0.5"/>
-        </group>
-        <group id_="806535232" open_="true" name="core2" pos="0.0 0.0 -0.275" rot="0.0 0.0 0.0">
-            <vox id_="378362432" pos="-0.025 -0.125 0.0" rot="0.0 0.0 0.0" file="MOD/physgun.vox" object="core_2" scale="0.5"/>
-        </group>
-        <group id_="1255943040" open_="true" name="arms_rot" pos="0.0 0.0 -0.375" rot="0.0 0.0 0.0">
-            <group id_="439970016" open_="true" name="arm0_base" pos="0.0 0.1 0.0" rot="0.0 0.0 0.0">
-                <vox id_="1925106432" pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_00" scale="0.5"/>
-                <group id_="2122316288" open_="true" name="arm0_tip" pos="0.0 0.2 -0.0" rot="0.0 0.0 0.0">
-                    <vox id_="572557440" pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_01" scale="0.5"/>
-                </group>
-            </group>
-            <group id_="516324128" open_="true" name="arm1_base" pos="0.087 -0.05 0.0" rot="180.0 180.0 -60.0">
-                <vox id_="28575440" pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_10" scale="0.5"/>
-                <group id_="962454912" open_="true" name="arm1_tip" pos="0.0 0.2 0.0" rot="0.0 0.0 0.0">
-                    <vox id_="1966724352" pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_11" scale="0.5"/>
-                </group>
-            </group>
-            <group id_="634361664" open_="true" name="arm2_base" pos="-0.087 -0.05 0.0" rot="180.0 180.0 60.0">
-                <vox id_="1049360960" pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_20" scale="0.5"/>
-                <group id_="1428116608" open_="true" name="arm2_tip" pos="0.0 0.2 0.0" rot="0.0 0.0 0.0">
-                    <vox id_="1388661504" pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_21" scale="0.5"/>
-                </group>
-            </group>
-        </group>
-        <group id_="1569551872" open_="true" name="nozzle" pos="0.0 0.0 -0.475">
-            <vox id_="506099872" pos="-0.025 -0.125 0.1" file="MOD/physgun.vox" object="cannon" scale="0.5"/>
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
- end)();
---src/tool.lua
-(function() 
-
----@class Tool
----@field _TRANSFORM Transformation
----@field _TRANSFORM_FIX Transformation
----@field _TRANSFORM_DIFF Transformation
----@field _ARMATURE Armature
----@field armature Armature
----@field _SHAPES Shape[]
----@field _OBJECTS table[]
----@field model string
----@field printname string
----@field id string
-local tool_meta = global_metatable( "tool" )
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
----@type table<string, Tool>
-local extra_tools = {}
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
-	RegisterTool( id, data.printname or id, data.model or "" )
-	SetBool( "game.tool." .. id .. ".enabled", true )
-	return data
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
- end)();
---src/_index.lua
-(function() 
--- UMF_REQUIRE "tdui"
- end)();
-for i = 1, #__RUNLATER do local f = loadstring(__RUNLATER[i]) if f then pcall(f) end end

```

---

# Migration Report: custom_robot\scripts\utility.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_robot\scripts\utility.lua
+++ patched/custom_robot\scripts\utility.lua
@@ -1,234 +1,36 @@
---[[VECTORS]]
+#version 2
+function VecDist(a, b) return VecLength(VecSub(a, b)) end
 
-    --- Distance between two vectors.
-    function VecDist(a, b) return VecLength(VecSub(a, b)) end
-    --- Divide a vector by another vector's components.
-    function VecDiv(a, b) return Vec(a[1] / b[1], a[2] / b[2], a[3] / b[3]) end
-    --- Add a table of vectors together.
-    function VecAddAll(vtb) local v = Vec(0,0,0) for i = 1, #vtb do VecAdd(v, vtb[i]) end return v end
-    --- Returns a vector with random values.
-    function VecRdm(length)
+function VecDiv(a, b) return Vec(a[1] / b[1], a[2] / b[2], a[3] / b[3]) end
+
+function VecAddAll(vtb) local v = Vec(0,0,0) for i = 1, #vtb do VecAdd(v, vtb[i]) end return v end
+
+function VecRdm(length)
         local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
         return VecScale(v, length)
     end
-    --- Print QuatEulers or vectors.
-    function VecPrint(vec, decimals, label)
+
+function VecPrint(vec, decimals, label)
         DebugPrint((label or "") ..
             "  " .. sfn(vec[1], decimals or 2) ..
             "  " .. sfn(vec[2], decimals or 2) ..
             "  " .. sfn(vec[3], decimals or 2))
     end
-    function VecApproach(startPos, endPos, speed)
+
+function VecApproach(startPos, endPos, speed)
         local subtractedPos = VecScale(VecNormalize(VecSub(endPos, startPos)), speed)
         return VecAdd(startPos, subtractedPos)
     end
-    function VecMult(vec1, vec2)
+
+function VecMult(vec1, vec2)
         local vec = Vec(0,0,0)
         for i = 1, 3 do vec[i] = vec1[i] * vec2[i] end
         return vec
     end
 
+function myDot(a, b) return (a[1] * b[1]) + (a[2] * b[2]) + (a[3] * b[3]) end
 
-    getCrosshairWorldPos = function(rejectBodies)
-
-        local crosshairTr = getCrosshairTr()
-        -- rejectAllBodies(rejectBodies)
-        local crosshairHit, crosshairHitPos = RaycastFromTransform(crosshairTr, 200)
-        if crosshairHit then
-            return crosshairHitPos
-        else
-            return nil
-        end
-
-    end
-
-    getCrosshairTr = function(pos, x, y)
-
-        pos = pos or GetCameraTransform()
-
-        local crosshairDir = UiPixelToWorld(x or UiCenter(), y or UiMiddle())
-        local crosshairQuat = DirToQuat(crosshairDir)
-        local crosshairTr = Transform(GetCameraTransform().pos, crosshairQuat)
-
-        return crosshairTr
-
-    end
-
-
-    function myDot(a, b) return (a[1] * b[1]) + (a[2] * b[2]) + (a[3] * b[3]) end
-    function myMag(a) return math.sqrt((a[1] * a[1]) + (a[2] * a[2]) + (a[3] * a[3])) end
-
---[[QUAT]]
-do
-    function QuatLookUp(pos) return QuatLookAt(pos, VecAdd(pos, Vec(0, 1, 0))) end
-    function QuatLookDown(pos) return QuatLookAt(pos, VecAdd(pos, Vec(0, -1, 0))) end
-
-    function QuatTrLookUp(tr) return QuatLookAt(tr.pos, TransformToParentPoint(tr, Vec(0,1,0))) end
-    function QuatTrLookDown(tr) return QuatLookAt(tr.pos, TransformToParentPoint(tr, Vec(0,-1,0))) end
-    function QuatTrLookLeft(tr) return QuatLookAt(tr.pos, TransformToParentPoint(tr, Vec(-1,0,0))) end
-    function QuatTrLookRight(tr) return QuatLookAt(tr.pos, TransformToParentPoint(tr, Vec(1,0,0))) end
-    function QuatTrLookBack(tr) return QuatLookAt(tr.pos, TransformToParentPoint(tr, Vec(0,0,1))) end
-
-    function QuatToDir(quat) return VecNormalize(TransformToParentPoint(Transform(Vec, quat), Vec(0,0,-1))) end -- Quat to normalized dir.
-    function DirToQuat(dir) return QuatLookAt(Vec(0, 0, 0), dir) end -- Normalized dir to quat.
-
-    function DirLookAt(eye, target) return VecNormalize(VecSub(eye, target)) end -- Normalized dir of two positions.
-
-    function VecAngle(a,b) -- Angle between two vectors.
-        local c = {a[1], a[2], a[3]}
-        local d = {b[1], b[2], b[3]}
-        return math.deg(math.acos(myDot(c, d) / (myMag(c) * myMag(d))))
-    end
-
-    function QuatAngle(a,b) -- Angle between two vectors.
-        av = QuatToDir(a)
-        bv = QuatToDir(b)
-        local c = {av[1], av[2], av[3]}
-        local d = {bv[1], bv[2], bv[3]}
-        return math.deg(math.acos(myDot(c, d) / (myMag(c) * myMag(d))))
-    end
-end
-
-
---[[AABB]]
-do
-    function AabbDimensions(min, max) return Vec(max[1] - min[1], max[2] - min[2], max[3] - min[3]) end
-    function AabbDraw(v1, v2, r, g, b, a)
-        r = r or 1
-        g = g or 1
-        b = b or 1
-        a = a or 1
-        local x1 = v1[1]
-        local y1 = v1[2]
-        local z1 = v1[3]
-        local x2 = v2[1]
-        local y2 = v2[2]
-        local z2 = v2[3]
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
-    function AabbCheckOverlap(aMin, aMax, bMin, bMax)
-        return
-        (aMin[1] <= bMax[1] and aMax[1] >= bMin[1]) and
-        (aMin[2] <= bMax[2] and aMax[2] >= bMin[2]) and
-        (aMin[3] <= bMax[3] and aMax[3] >= bMin[3])
-    end
-    function AabbCheckPointInside(aMin, aMax, pos)
-        return
-        (pos[1] <= aMax[1] and pos[1] >= aMin[1]) and
-        (pos[2] <= aMax[2] and pos[2] >= aMin[2]) and
-        (pos[3] <= aMax[3] and pos[3] >= aMin[3])
-    end
-    function AabbClosestEdge(pos, shape)
-
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
-    function AabbSortEdges(startPos, endPos, edges)
-        local s, startIndex = aabbClosestEdge(startPos, edges)
-        local e, endIndex = aabbClosestEdge(endPos, edges)
-        --- Swap first index with startPos and last index with endPos. Everything between stays same.
-        edges = tableSwapIndex(edges, 1, startIndex)
-        edges = tableSwapIndex(edges, #edges, endIndex)
-        return edges
-    end
-    function AabbGetShapeCenterPos(shape)
-        local mi, ma = GetShapeBounds(shape)
-        return VecLerp(mi,ma,0.5)
-    end
-    function AabbGetBodyCenterPos(body)
-        local mi, ma = GetBodyBounds(body)
-        return VecLerp(mi,ma,0.5)
-    end
-    function AabbGetShapeCenterTopPos(shape, addY)
-        addY = addY or 0
-        local mi, ma = GetShapeBounds(shape)
-        local v =  VecLerp(mi,ma,0.5)
-        v[2] = ma[2] + addY
-        return v
-    end
-    function AabbGetBodyCenterTopPos(body, addY)
-        addY = addY or 0
-        local mi, ma = GetBodyBounds(body)
-        local v =  VecLerp(mi,ma,0.5)
-        v[2] = ma[2] + addY
-        return v
-    end
-end
-
---[[OBB]]
-do
-    function ObbDrawShape(shape)
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
---[[TABLES]]
-do
-    function TableSwapIndex(t, i1, i2)
-        local temp = t[i1]
-        t[i1] = t[i2]
-        t[i2] = temp
-        return t
-    end
-    function TableClone(tb)
-        local tbc = {}
-        for k,v in pairs(tb) do tbc[k] = v end
-        return tbc
-    end
-end
+function myMag(a) return math.sqrt((a[1] * a[1]) + (a[2] * a[2]) + (a[3] * a[3])) end
 
 function DeepCopy(orig)
     local orig_type = type(orig)
@@ -245,8 +47,6 @@
     return copy
 end
 
----@param t table -- table to print
----@param n number -- recursion depth (leave as 0)
 function printTable(t, n)
 
     n = n or 0
@@ -283,238 +83,17 @@
 
 end
 
-
 function GetRandomIndex(tb)
     return tb[math.random(1, #tb)]
 end
 
-
-
---[[QUERY]]
-do
-    ---comment
-    ---@param tr table -- Source transform.
-    ---@param distance number -- Max raycast distance. Default is 300.
-    ---@param rad number -- Raycst radius.
-    ---@param rejectBodies table -- Table of bodies to reject.
-    ---@param rejectShapes table -- Table of shapes to reject.
-    ---@param returnNil bool -- If true, return nil if no raycast hit. If false, return the end point of the raycast based on the transfom and distance.
-    ---@return hit boolean
-    ---@return hitPos table
-    ---@return hitShape table
-    ---@return hitBody table
-    ---@return hitDist number
-    function RaycastFromTransform(tr, distance, rad, rejectBodies, rejectShapes, returnNil)
-
-        if distance == nil then distance = 300 end
-
-        if rejectBodies ~= nil then for i = 1, #rejectBodies do QueryRejectBody(rejectBodies[i]) end end
-        if rejectShapes ~= nil then for i = 1, #rejectShapes do QueryRejectShape(rejectShapes[i]) end end
-
-        returnNil = returnNil or false
-
-        local direction = QuatToDir(tr.rot)
-        local h, d, n, s = QueryRaycast(tr.pos, direction, distance, rad)
-        if h then
-            local p = TransformToParentPoint(tr, Vec(0, 0, d * -1))
-            local b = GetShapeBody(s)
-            return h, p, s, b, d, n
-        elseif not returnNil then
-            return true, TransformToParentPoint(tr, Vec(0,0,-300))
-        else
-            return nil
-        end
-    end
-
-end
-
-
-
---[[PHYSICS]]
-do
-    -- Reduce the angular body velocity by a certain rate each frame.
-    function DiminishBodyAngVel(body, rate)
-        local angVel = GetBodyAngularVelocity(body)
-        local dRate = rate or 0.99
-        local diminishedAngVel = Vec(angVel[1]*dRate, angVel[2]*dRate, angVel[3]*dRate)
-        SetBodyAngularVelocity(body, diminishedAngVel)
-    end
-    function IsMaterialUnbreakable(mat, shape)
-        return mat == 'rock' or mat == 'heavymetal' or mat == 'unbreakable' or mat == 'hardmasonry' or
-            HasTag(shape,'unbreakable') or HasTag(GetShapeBody(shape),'unbreakable')
-    end
-end
-
-
---[[VFX]]
-do
-    colors = {
-        white = Vec(1,1,1),
-        black = Vec(0,0,0),
-        grey = Vec(0,0,0),
-        red = Vec(1,0,0),
-        blue = Vec(0,0,1),
-        yellow = Vec(1,1,0),
-        purple = Vec(1,0,1),
-        green = Vec(0,1,0),
-        orange = Vec(1,0.5,0),
-    }
-    function DrawDot(pos, l, w, r, g, b, a, dt)
-        local dot = LoadSprite("ui/hud/dot-small.png")
-        local spriteRot = QuatLookAt(pos, GetCameraTransform().pos)
-        local spriteTr = Transform(pos, spriteRot)
-        if dt == nil then dt = true end
-        DrawSprite(dot, spriteTr, l or 0.2, w or 0.2, r or 1, g or 1, b or 1, a or 1, dt and true)
-    end
-end
-
-
-
---[[SOUND]]
-do
-    function beep(pos, vol) PlaySound(LoadSound("warning-beep"), pos or GetCameraTransform().pos, vol or 0.3) end
-    function buzz(pos, vol) PlaySound(LoadSound("light/spark0"), pos or GetCameraTransform().pos, vol or 0.3) end
-    function chime(pos, vol) PlaySound(LoadSound("elevator-chime"), pos or GetCameraTransform().pos, vol or 0.3) end
-    function shine(pos, vol) PlaySound(LoadSound("valuable.ogg"), pos or GetCameraTransform().pos, vol or 0.3) end
-end
-
-
-
---[[MATH]]
-do
-    function round(n, dec) local pow = 10^dec return math.floor(n * pow) / pow end
-    --- return number if > 0, else return 0.00000001
-    function gtZero(n) if n <= 0 then return 0.00000001 end return n end
-    --- return number if not = 0, else return 0.00000001
-    function nZero(n) if n == 0 then return 0.00000001 end return n end
-
-    function rdm(min, max)
-        return math.random(min, max-1) + math.random()
-    end
-    function clamp(value, mi, ma)
-        if value < mi then value = mi end
-        if value > ma then value = ma end
-        return value
-    end
-    function oscillate(time)
-        local a = (GetTime() / (time or 1)) % 1
-        a = a * math.pi
-        return math.sin(a)
-    end
-
-    ---@param x number
-    ---@param hScale number
-    function GetParabola(x, hScale)
-        local h = 1
-        local w = 0
-        local s = 1
-        local y = (-(4*h-w) * (x-(1/2)*s)^2 + (4*h/4)) * hScale
-        return y
-    end
-
-    function DrawParabola()
-        local scale = 3
-        local hScale = 4
-        local denisty = 10 * scale
-        for i = 0, 1, 1/denisty do
-            local pos = Vec(i, 0, 0)
-            pos[2] = GetParabola(i, hScale)
-            pos = VecScale(pos, scale)
-
-            DrawDot(pos, 0.2,0.2, 0,1,1, 1, false)
-        end
-    end
-
-    function Round(x, n)
-        n = math.pow(10, n or 0)
-        x = x * n
-        if x >= 0 then x = math.floor(x + 0.5) else x = math.ceil(x - 0.5) end
-        return x / n
-    end
-end
-
-
-
---[[LOGIC]]
-do
-    function ternary ( cond , T , F )
-        if cond then return T else return F end
-    end
-end
-
-
-
-
---[[FORMATTING]]
-do
-    --- string format. default 2 decimals.
-    function sfn(numberToFormat, dec)
-        local s = (tostring(dec or 2))
-        return string.format("%."..s.."f", numberToFormat)
-    end
-    function sfnTime(dec) return sfn(' '..GetTime(), dec or 4) end
-    function sfnCommas(dec)
-        return tostring(math.floor(dec)):reverse():gsub("(%d%d%d)","%1,"):gsub(",(%-?)$","%1"):reverse()
-        -- https://stackoverflow.com/questions/10989788/format-integer-in-lua
-    end
-end
-
-
-
-
---[[TIMERS]]
-do
-
-    function TimerCreate(time, rpm)
-        return {time = time, rpm = rpm}
-    end
-
-    ---Run a timer and a table of functions.
-    ---@param timer table -- = {time, rpm}
-    ---@param functions table -- Table of functions that are called when time = 0.
-    ---@param runTime boolean -- Decrement time when calling this function.
-    function TimerRunTimer(timer, functions, runTime)
-        if timer.time <= 0 then
-            TimerResetTime(timer)
-
-            for i = 1, #functions do
-                functions[i]()
-            end
-
-        elseif runTime then
-            TimerRunTime(timer)
-        end
-    end
-
-    -- Only runs the timer countdown if there is time left.
-    function TimerRunTime(timer)
-        if timer.time > 0 then
-            timer.time = timer.time - GetTimeStep()
-        end
-    end
-
-    -- Set time left to 0.
-    function TimerEndTime(timer)
-        timer.time = 0
-    end
-
-    -- Reset time to start (60/rpm).
-    function TimerResetTime(timer)
-        timer.time = 60/timer.rpm
-    end
-end
-
-
-
---[[TOOL]]
----Disable all tools except specified ones.
----@param allowTools table -- Table of strings (tool names) to not disable.
 function disableTools(allowTools)
     local toolNames = {sledge = 'sledge', spraycan = 'spraycan', extinguisher ='extinguisher', blowtorch = 'blowtorch'}
     local tools = ListKeys("game.tool")
     for i=1, #tools do
         if tools[i] ~= toolNames[tools[i]] then
-            SetBool("game.tool."..tools[i]..".enabled", false)
+            SetBool("game.tool."..tools[i]..".enabled", false, true)
         end
     end
 end
+

```

---

# Migration Report: custom_robot\scripts\version.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_robot\scripts\version.lua
+++ patched/custom_robot\scripts\version.lua
@@ -0,0 +1 @@
+#version 2

```

---

# Migration Report: custom_robot\scripts\weapons.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_robot\scripts\weapons.lua
+++ patched/custom_robot\scripts\weapons.lua
@@ -1,8 +1,4 @@
-activeMissiles = {}
-activeBullets = {}
-
-
---[[BULLETS]]
+#version 2
 function createBullet(transform, activeBullets, bulletPreset, ignoreBodies) --- Instantiates a bullet and adds it to the activeBullets table
 
     local bullet = TableClone(bulletPreset)
@@ -12,6 +8,7 @@
     table.insert(activeBullets, bullet)
 
 end
+
 function manageActiveBullets(activeBullets)
     if #activeBullets >= 1 then
 
@@ -42,6 +39,7 @@
     end
 
 end
+
 function propelBullet(bullet)
 
     if bullet.ignoreBodies ~= nil then -- TODO append different tags to table
@@ -86,7 +84,7 @@
         MakeHole(hitPos, holeSize, holeSize, holeSize, holeSize)
         PointLight(hitPos, bullet.particleColor[1], bullet.particleColor[2], bullet.particleColor[3], 3)
 
-        if bullet.explosive > 0 then
+        if bullet.explosive ~= 0 then
             Explosion(hitPos, bullet.explosive)
         end
 
@@ -135,8 +133,6 @@
 
 end
 
-
---[[MISSILES]]
 function createMissile(transform, activeMissiles, missilePreset, ignoreBodies)
     --- Instantiates a missile and adds it to the activeMissiles table
 
@@ -146,6 +142,7 @@
 
     table.insert(activeMissiles, missile)
 end
+
 function manageActiveMissiles(activeMissiles)
     if #activeMissiles >= 1 then
 
@@ -175,6 +172,7 @@
 
     end
 end
+
 function propelMissile(missile)
 
     missile.transform.pos = TransformToParentPoint(missile.transform, Vec(0,-missile.dropOff,-missile.speed))
@@ -249,7 +247,6 @@
 
     missile.transform.pos = TransformToParentPoint(missile.transform, Vec(0,0,-missile.speed))
 end
-
 
 function initWeapons()
 
@@ -346,7 +343,9 @@
     }
 
 end
+
 function manageProjs()
     manageActiveBullets(activeBullets)
     manageActiveMissiles(activeMissiles)
 end
+

```

---

# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,22 +1,4 @@
-#include "custom_robot/scripts/robot.lua"
-
-
-function init()
-
-    -- Check if map has has an existing robot.
-    local robotBodies = FindBodies('robotVehicle', true)
-    if #robotBodies >= 1 then
-        SetBool('level.robotExists', true)
-        dbp('Map includes existing robot.')
-    end
-
-end
-
-function tick()
-    manageRobotSpawning()
-end
-
-
+#version 2
 function manageRobotSpawning()
 
     if HasVersion("0.9.3") and regGetBool('spawningKeysEnabled') then
@@ -25,16 +7,31 @@
         if InputPressed(regGetString('options.keys.spawnMenu')) then
             local hit, pos = RaycastFromTransform(GetCameraTransform())
             Spawn('MOD/custom_robot/robot/mech-aeon.xml', Transform(pos))
-            SetBool('level.robotExists', true)
+            SetBool('level.robotExists', true, true)
         end
 
         -- Spawn mech-aeon
         if InputPressed(regGetString('options.keys.quickSpawn')) then
             local hit, pos = RaycastFromTransform(GetCameraTransform())
             Spawn('MOD/custom_robot/instance_robotVehicle.xml', Transform(pos))
-            SetBool('level.robotExists', true)
+            SetBool('level.robotExists', true, true)
         end
 
     end
 
 end
+
+function server.init()
+    local robotBodies = FindBodies('robotVehicle', true)
+    if #robotBodies >= 1 then
+        SetBool('level.robotExists', true, true)
+        dbp('Map includes existing robot.')
+    end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        manageRobotSpawning()
+    end
+end
+

```

---

# Migration Report: menu.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/menu.lua
+++ patched/menu.lua
@@ -1,66 +1,4 @@
-function init()
-
-    menu = {
-
-        isShowing = true,
-
-        map = {
-            campaign = false,
-            sandbox = false,
-        },
-
-    }
-
-
-    ui = {
-        text = {
-            size = {
-                s = 12,
-                m = 24,
-                l = 48,
-            },
-        },
-        container = {
-            width = 1440,
-            height = 240,
-        },
-        padding = 25,
-        colors = {
-            text = 1,
-            fg = 0.3,
-            bg = 0.12,
-        },
-        grid = {
-            createNewRow = function ()
-                UiTranslate(-580, 150)
-            end,
-            insertColPadding = function ()
-                UiTranslate(20, 0)
-            end,
-        }
-    }
-
-end
-
-
-function tick()
-    UiMakeInteractive()
-
-    if menu.map.campaign then
-        StartLevel('', "MOD/testLevel.xml")
-    elseif menu.map.sandbox then
-        StartLevel('', "MOD/miniCity.xml")
-    end
-end
-
-
-function draw()
-    drawBackground()
-    drawHeader()
-    drawMenu()
-end
-
-
+#version 2
 function drawMenu()
 
     -- CAMPAIGN
@@ -91,9 +29,7 @@
 
     UiPop()
 
-
     UiTranslate(740, 0)
-
 
     -- CAMPAIGN
     UiPush()
@@ -125,12 +61,10 @@
 
 end
 
-
 function drawBackground()
     UiColor(0,0,0,1)
     UiRect(UiWidth(),UiHeight())
 end
-
 
 function drawHeader()
     UiTranslate(240, 45)
@@ -165,3 +99,65 @@
 
     UiTranslate(0, 205)
 end
+
+function server.init()
+    menu = {
+        isShowing = true,
+        map = {
+            campaign = false,
+            sandbox = false,
+        },
+    }
+    ui = {
+        text = {
+            size = {
+                s = 12,
+                m = 24,
+                l = 48,
+            },
+        },
+        container = {
+            width = 1440,
+            height = 240,
+        },
+        padding = 25,
+        colors = {
+            text = 1,
+            fg = 0.3,
+            bg = 0.12,
+        },
+        grid = {
+            createNewRow = function ()
+            end,
+            insertColPadding = function ()
+            end,
+        }
+    }
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if menu.map.campaign then
+            StartLevel('', "MOD/testLevel.xml")
+        elseif menu.map.sandbox then
+            StartLevel('', "MOD/miniCity.xml")
+        end
+    end
+end
+
+function client.init()
+    UiTranslate(-580, 150)
+    UiTranslate(20, 0)
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    UiMakeInteractive()
+end
+
+function client.draw()
+    drawBackground()
+    drawHeader()
+    drawMenu()
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
@@ -1,141 +1,15 @@
-#include "custom_robot/scripts/registry.lua"
-#include "custom_robot/scripts/utility.lua"
-
-
-function init()
-
-    checkRegInitialized()
-
-    activeAssignment = false
-    activePath = '.'
-    lastKeyPressed = '.'
-
-    font_size = 32
-
-end
-
-function tick()
-
-    manageKeyAssignment()
-
-    -- DebugWatch('reg val', regGetString('options.keys.spawnMenu'))
-    -- DebugWatch('InputLastPressedKey', lastKeyPressed)
-    -- DebugWatch('activeAssignment', activeAssignment)
-    -- DebugWatch('activePath', activePath)
-    -- DebugWatch('oscillate(GetTime())', oscillate(GetTime()))
-
-end
-
+#version 2
 function manageKeyAssignment()
 
     if activeAssignment and InputLastPressedKey() ~= '' then
 
-        regSetString(activePath, string.lower(InputLastPressedKey()))
+        regSetString(activePath, string.lower(InputLastPressedKey()), true)
         activeAssignment = false
         activePath = ''
 
     end
 
 end
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
-        UiTranslate(0, font_size)
-        do UiPush()
-            UiFont('regular.ttf', 64)
-            UiAlign('center top')
-            UiText('Robot Vehicles Options')
-        UiPop() end
-
-        UiTranslate(0, 200)
-
-        do UiPush()
-
-            local c = oscillate(2)/3 + 2/3
-            UiColor(c,c,1,1)
-            UiAlign('center middle')
-            UiFont('regular.ttf', font_size*1.5)
-
-            UiButtonImageBox("ui/common/box-outline-6.png", 10,10)
-            UiButtonHoverColor(0.5,0.5,1,1)
-            if UiTextButton('Start Demo Map', 350, font_size*2.5) then
-                StartLevel('', 'demo.xml', '')
-            end
-
-        UiPop() end
-
-        UiTranslate(0, 200)
-
-        -- Version warning.
-        if HasVersion("0.9.3") then
-
-            ui_createToggleSwitch('Enable keybind spawning.', 'spawningKeysEnabled', font_size)
-
-            if regGetBool('spawningKeysEnabled') then
-
-                UiTranslate(0, font_size*2.5)
-                Ui_Option_Keybind('Spawn Basic Robot', 'options.keys.spawnMenu')
-
-                UiTranslate(0, font_size*2.5)
-                Ui_Option_Keybind('Spawn Aeon Robot', 'options.keys.quickSpawn')
-
-            end
-
-
-        else
-
-            do UiPush()
-
-                UiColor(1,0,0,1)
-                UiAlign('center middle')
-                UiFont('regular.ttf', font_size)
-                UiTranslate(0, font_size*2)
-
-                UiText('Spawning unavailable!')
-                UiTranslate(0, font_size*1.5)
-
-                UiText('Please switch to the Teardown experimental beta in Steam to enable spawning.')
-
-
-            UiPop() end
-
-        end
-
-
-    UiPop() end
-
-
-    do UiPush()
-
-        UiTranslate(0, -100)
-
-        UiTranslate(0, UiHeight() - font_size*2.5)
-        UiAlign('center middle')
-        UiButtonImageBox("ui/common/box-outline-6.png", 10,10)
-        UiButtonHoverColor(0.5,0.5,1,1)
-        if UiTextButton('Reset Options', 200, font_size*2) then
-            optionsReset()
-        end
-
-        UiTranslate(0, font_size*2.5)
-        UiAlign('center middle')
-        UiButtonImageBox("ui/common/box-outline-6.png", 10,10)
-        UiButtonHoverColor(0.5,0.5,1,1)
-        if UiTextButton('Close', 150, font_size*2) then
-            Menu()
-        end
-
-    UiPop() end
-
-end
-
 
 function Ui_Option_Keybind(label, regPath)
 
@@ -155,7 +29,7 @@
         if UiTextButton(regGetString(regPath), font_size*6, font_size*2) then
 
             if not activeAssignment then
-                regSetString(regPath, 'Press key...')
+                regSetString(regPath, 'Press key...', true)
                 activeAssignment = true
                 activePath = regPath
             end
@@ -165,7 +39,6 @@
     UiPop() end
 
 end
-
 
 function ui_createToggleSwitch(title, registryPath, fontSize)
 
@@ -180,7 +53,6 @@
         UiFont('regular.ttf', fontSize)
         UiText(title)
         UiTranslate(font_size, -fontSize/2)
-
 
         -- Toggle BG
         UiAlign('left top')
@@ -216,10 +88,116 @@
 
         UiButtonImageBox('ui/common/box-outline-6.png', 10,10, 0,0,0, a)
         if UiBlankButton(tglW, tglH) then
-            SetBool('savegame.mod.' .. registryPath, not value)
+            SetBool('savegame.mod.' .. registryPath, not value, true)
             PlaySound(LoadSound('clickdown.ogg'), GetCameraTransform().pos, 1)
         end
 
     UiPop() end
 
-end+end
+
+function server.init()
+    checkRegInitialized()
+    activeAssignment = false
+    activePath = '.'
+    lastKeyPressed = '.'
+    font_size = 32
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        manageKeyAssignment()
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
+        UiTranslate(0, font_size)
+        do UiPush()
+            UiFont('regular.ttf', 64)
+            UiAlign('center top')
+            UiText('Robot Vehicles Options')
+        UiPop() end
+
+        UiTranslate(0, 200)
+
+        do UiPush()
+
+            local c = oscillate(2)/3 + 2/3
+            UiColor(c,c,1,1)
+            UiAlign('center middle')
+            UiFont('regular.ttf', font_size*1.5)
+
+            UiButtonImageBox("ui/common/box-outline-6.png", 10,10)
+            UiButtonHoverColor(0.5,0.5,1,1)
+            if UiTextButton('Start Demo Map', 350, font_size*2.5) then
+                StartLevel('', 'demo.xml', '')
+            end
+
+        UiPop() end
+
+        UiTranslate(0, 200)
+
+        -- Version warning.
+        if HasVersion("0.9.3") then
+
+            ui_createToggleSwitch('Enable keybind spawning.', 'spawningKeysEnabled', font_size)
+
+            if regGetBool('spawningKeysEnabled') then
+
+                UiTranslate(0, font_size*2.5)
+                Ui_Option_Keybind('Spawn Basic Robot', 'options.keys.spawnMenu')
+
+                UiTranslate(0, font_size*2.5)
+                Ui_Option_Keybind('Spawn Aeon Robot', 'options.keys.quickSpawn')
+
+            end
+
+        else
+
+            do UiPush()
+
+                UiColor(1,0,0,1)
+                UiAlign('center middle')
+                UiFont('regular.ttf', font_size)
+                UiTranslate(0, font_size*2)
+
+                UiText('Spawning unavailable!')
+                UiTranslate(0, font_size*1.5)
+
+                UiText('Please switch to the Teardown experimental beta in Steam to enable spawning.')
+
+            UiPop() end
+
+        end
+
+    UiPop() end
+
+    do UiPush()
+
+        UiTranslate(0, -100)
+
+        UiTranslate(0, UiHeight() - font_size*2.5)
+        UiAlign('center middle')
+        UiButtonImageBox("ui/common/box-outline-6.png", 10,10)
+        UiButtonHoverColor(0.5,0.5,1,1)
+        if UiTextButton('Reset Options', 200, font_size*2) then
+            optionsReset()
+        end
+
+        UiTranslate(0, font_size*2.5)
+        UiAlign('center middle')
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

# Migration Report: tdapi.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/tdapi.lua
+++ patched/tdapi.lua
@@ -1,4015 +1,748 @@
----No Description
----
---- ---
---- Example
----```lua
------Retrieve blinkcount parameter, or set to 5 if omitted
----parameterBlinkCount = GetIntParam("blinkcount", 5)
----```
----@param name string
----@param default number
----@return number value
+#version 2
 function GetIntParam(name, default) end
 
----No Description
----
---- ---
---- Example
----```lua
------Retrieve speed parameter, or set to 10.0 if omitted
----parameterSpeed = GetFloatParam("speed", 10.0)
----```
----@param name string
----@param default number
----@return number value
 function GetFloatParam(name, default) end
 
----No Description
----
---- ---
---- Example
----```lua
------Retrieve playsound parameter, or false if omitted
----parameterPlaySound = GetBoolParam("playsound", false)
----```
----@param name string
----@param default boolean
----@return boolean value
 function GetBoolParam(name, default) end
 
----No Description
----
---- ---
---- Example
----```lua
------Retrieve mode parameter, or "idle" if omitted
----parameterMode = GetSrtingParam("mode", "idle")
----```
----@param name string
----@param default string
----@return string value
 function GetStringParam(name, default) end
 
----No Description
----
---- ---
---- Example
----```lua
----local v = GetVersion()
------v is "0.5.0"
----```
----@return string version
 function GetVersion() end
 
----No Description
----
---- ---
---- Example
----```lua
----if HasVersion("0.6.0") then
----	--conditional code that only works on 0.6.0 or above
----else
----	--legacy code that works on earlier versions
----end
----```
----@param version string
----@return boolean match
 function HasVersion(version) end
 
----Returns running time of this script. If called from update, this returns
----the simulated time, otherwise it returns wall time.
----
---- ---
---- Example
----```lua
----local t = GetTime()
----```
----@return number time
 function GetTime() end
 
----Returns timestep of the last frame. If called from update, this returns
----the simulation time step, which is always one 60th of a second (0.0166667).
----If called from tick or draw it returns the actual time since last frame.
----
---- ---
---- Example
----```lua
----local dt = GetTimeStep()
----```
----@return number dt
 function GetTimeStep() end
 
----No Description
----
---- ---
---- Example
----```lua
----name = InputLastPressedKey()
----```
----@return string name
 function InputLastPressedKey() end
 
----No Description
----
---- ---
---- Example
----```lua
----if InputPressed("interact") then
----	...
----end
----```
----@param input string
----@return boolean pressed
 function InputPressed(input) end
 
----No Description
----
---- ---
---- Example
----```lua
----if InputReleased("interact") then
----	...
----end
----```
----@param input string
----@return boolean pressed
 function InputReleased(input) end
 
----No Description
----
---- ---
---- Example
----```lua
----if InputDown("interact") then
----...
----end
----```
----@param input string
----@return boolean pressed
 function InputDown(input) end
 
----No Description
----
---- ---
---- Example
----```lua
----scrollPos = scrollPos + InputValue("mousewheel")
----```
----@param input string
----@return number value
 function InputValue(input) end
 
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
----@param variable string
----@param value number
----@param transition string
----@param time number
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
----@param title string
----@return boolean
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
----@param mission string
----@param path string
----@param layers string
-function StartLevel(mission, path, layers) end
-
----Set paused state of the game
----
---- ---
---- Example
----```lua
------Pause game and bring up pause menu on HUD
----SetPaused(true)
----```
----@param paused boolean
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
----@param key string
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
----@param parent string
----@return table children
-function ListKeys(parent) end
-
----Returns true if the registry contains a certain key
----
---- ---
---- Example
----```lua
----local foo = HasKey("score.levels")
----```
----@param key string
----@return boolean exists
-function HasKey(key) end
-
----No Description
----
---- ---
---- Example
----```lua
----SetInt("score.levels.level1", 4)
----```
----@param key string
----@param value number
-function SetInt(key, value) end
-
----No Description
----
---- ---
---- Example
----```lua
----local a = GetInt("score.levels.level1")
----```
----@param key string
----@return number value
-function GetInt(key) end
-
----No Description
----
---- ---
---- Example
----```lua
----SetFloat("level.time", 22.3)
----```
----@param key string
----@param value number
-function SetFloat(key, value) end
-
----No Description
----
---- ---
---- Example
----```lua
----local time = GetFloat("level.time")
----```
----@param key string
----@return number value
-function GetFloat(key) end
-
----No Description
----
---- ---
---- Example
----```lua
----SetBool("level.robots.enabled", true)
----```
----@param key string
----@param value boolean
-function SetBool(key, value) end
-
----No Description
----
---- ---
---- Example
----```lua
----local isRobotsEnabled = GetBool("level.robots.enabled")
----```
----@param key string
----@return boolean value
-function GetBool(key) end
-
----No Description
----
---- ---
---- Example
----```lua
----SetString("level.name", "foo")
----```
----@param key string
----@param value string
-function SetString(key, value) end
-
----No Description
----
---- ---
---- Example
----```lua
----local name = GetString("level.name")
----```
----@param key string
----@return string value
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
----@param x number
----@param y number
----@param z number
----@return table vec
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
----@param org table
----@return table new
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
----@param vec table
----@return number length
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
----@param vec table
----@return table norm
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
----@param vec table
----@param scale number
----@return table norm
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
----@param a table
----@param b table
----@return table c
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
----@param a table
----@param b table
----@return table c
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
----@param a table
----@param b table
----@return number c
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
----@param a table
----@param b table
----@return table c
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
----@param a table
----@param b table
----@param t number
----@return table c
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
----@param x number
----@param y number
----@param z number
----@param w number
----@return table quat
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
----@param org table
----@return table new
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
----@param axis table
----@param angle number
----@return table quat
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
----@param x number
----@param y number
----@param z number
----@return table quat
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
----@param quat table
----@return number x
----@return number y
----@return number z
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
----@param eye table
----@param target table
----@return table quat
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
----@param a table
----@param b table
----@param t number
----@return table c
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
----@param a table
----@param b table
----@return table c
-function QuatRotateQuat(a, b) end
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
----@param pos table
----@param rot table
----@return table transform
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
----@param org table
----@return table new
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
----@param parent table
----@param child table
----@return table transform
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
----@param parent table
----@param child table
----@return table transform
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
----@param t table
----@param v table
----@return table r
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
----@param t table
----@param v table
----@return table r
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
----@param t table
----@param p table
----@return table r
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
----@param t table
----@param p table
----@return table r
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
----@param handle number
----@param tag string
----@param value string
-function SetTag(handle, tag, value) end
-
----Remove tag from an entity. If the tag had a value it is removed too.
----
---- ---
---- Example
----```lua
----RemoveTag(handle, "special")
----```
----@param handle number
----@param tag string
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
----@param handle number
----@param tag string
----@return boolean exists
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
----@param handle number
----@param tag string
----@return string value
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
----@param handle number
----@return string description
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
----@param handle number
----@param description string
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
----@param handle number
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
----@param handle number
----@return boolean exists
-function IsHandleValid(handle) end
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
----@param tag string
----@param global boolean
----@return number handle
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
----@param tag string
----@param global boolean
----@return table list
-function FindBodies(tag, global) end
-
----No Description
----
---- ---
---- Example
----```lua
----local t = GetBodyTransform(body)
----```
----@param handle number
----@return table transform
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
----@param handle number
----@param transform table
-function SetBodyTransform(handle, transform) end
-
----No Description
----
---- ---
---- Example
----```lua
----local mass = GetBodyMass(body)
----```
----@param handle number
----@return number mass
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
----@param handle number
----@return boolean dynamic
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
----@param handle number
----@param dynamic boolean
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
----@param handle number
----@param velocity table
-function SetBodyVelocity(handle, velocity) end
-
----No Description
----
---- ---
---- Example
----```lua
----local linVel = GetBodyVelocity(body)
----```
----@param handle number
----@return table velocity
-function GetBodyVelocity(handle) end
-
----Return the velocity on a body taking both linear and angular velocity into account.
----
---- ---
---- Example
----```lua
----local vel = GetBodyVelocityAtPos(body, pos)
----```
----@param handle number
----@param pos table
----@return table velocity
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
----@param handle number
----@param angVel table
-function SetBodyAngularVelocity(handle, angVel) end
-
----No Description
----
---- ---
---- Example
----```lua
----local angVel = GetBodyAngularVelocity(body)
----```
----@param handle number
----@return table angVel
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
----@param handle number
----@return boolean active
-function IsBodyActive(handle) end
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
----@param handle number
----@param position table
----@param impulse table
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
----@param handle number
----@return table list
-function GetBodyShapes(handle) end
-
----No Description
----
---- ---
---- Example
----```lua
----local vehicle = GetBodyVehicle(body)
----```
----@param body number
----@return number handle
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
----@param handle number
----@return table min
----@return table max
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
----@param handle number
----@return table point
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
----@param handle number
----@param maxDist number
----@param rejectTransparent boolean
----@return boolean visible
-function IsBodyVisible(handle, maxDist, rejectTransparent) end
-
----Determine if any shape of a body has been broken.
----
---- ---
---- Example
----```lua
----local broken = IsBodyBroken(body)
----```
----@param handle number
----@return boolean broken
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
----@param handle number
----@return boolean result
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
----@param handle number
----@param r number
----@param g number
----@param b number
----@param a number
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
----@param handle number
----@param amount number
-function DrawBodyHighlight(handle, amount) end
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
----@param tag string
----@param global boolean
----@return number handle
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
----@param tag string
----@param global boolean
----@return table list
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
----@param handle number
----@return table transform
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
----@param handle number
----@param transform table
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
----@param handle number
----@return table transform
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
----@param handle number
----@return number handle
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
----@param shape number
----@return table list
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
----@param shape number
----@return table list
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
----@param handle number
----@return table min
----@return table max
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
----@param handle number
----@param scale number
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
----@param handle number
----@param pos table
----@return string type
----@return number r
----@return number g
----@return number b
----@return number a
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
----@param handle number
----@param x number
----@param y number
----@param z number
----@return string type
----@return number r
----@return number g
----@return number b
----@return number a
-function GetShapeMaterialAtIndex(handle, x, y, z) end
-
----This will return the closest point of a specific shape
----
---- ---
---- Example
----```lua
----local hit, p, n = GetShapeClosestPoint(s, Vec(0, 5, 0))
----if hit then
------Point p of shape s is closest to (0,5,0)
----end
----```
----@param shape number
----@param origin table
----@param maxDist number
----@return boolean hit
----@return table point
----@return table normal
-function GetShapeClosestPoint(shape, origin, maxDist) end
-
----Return the size of a shape in voxels
----
---- ---
---- Example
----```lua
----local x, y, z = GetShapeSize(shape)
----```
----@param handle number
----@return number xsize
----@return number ysize
----@return number zsize
----@return number scale
-function GetShapeSize(handle) end
-
----Return the number of voxels in a shape, not including empty space
----
---- ---
---- Example
----```lua
----local voxelCount = GetShapeVoxelCount(shape)
----```
----@param handle number
----@return number count
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
----@param handle number
----@param maxDist number
----@param rejectTransparent boolean
----@return boolean visible
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
----@param handle number
----@return boolean broken
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
----@param handle number
----@param r number
----@param g number
----@param b number
----@param a number
-function DrawShapeOutline(handle, r, g, b, a) end
-
----Flash the appearance of a shape when rendering this frame.
----
---- ---
---- Example
----```lua
----DrawShapeHighlight(shape, 0.5)
----```
----@param handle number
----@param amount number
-function DrawShapeHighlight(handle, amount) end
-
----No Description
----
---- ---
---- Example
----```lua
----local loc = FindLocation("start")
----```
----@param tag string
----@param global boolean
----@return number handle
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
----@param tag string
----@param global boolean
----@return table list
-function FindLocations(tag, global) end
-
----No Description
----
---- ---
---- Example
----```lua
----local t = GetLocationTransform(loc)
----```
----@param handle number
----@return table transform
-function GetLocationTransform(handle) end
-
----No Description
----
---- ---
---- Example
----```lua
----local joint = FindJoint("doorhinge")
----```
----@param tag string
----@param global boolean
----@return number handle
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
----@param tag string
----@param global boolean
----@return table list
-function FindJoints(tag, global) end
-
----No Description
----
---- ---
---- Example
----```lua
----local broken = IsJointBroken(joint)
----```
----@param joint number
----@return boolean broken
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
----@param joint number
----@return string type
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
----@param joint number
----@param shape number
----@return number other
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
----@param joint number
----@param velocity number
----@param strength number
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
----@param joint number
----@param target number
----@param maxVel number
----@param strength number
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
----@param joint number
----@return number min
----@return number max
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
----@param joint number
----@return number movement
-function GetJointMovement(joint) end
-
----No Description
----
---- ---
---- Example
----```lua
----local light = FindLight("main")
----```
----@param tag string
----@param global boolean
----@return number handle
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
----@param tag string
----@param global boolean
----@return table list
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
----@param handle number
----@param enabled boolean
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
----@param handle number
----@param r number
----@param g number
----@param b number
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
----@param handle number
----@param intensity number
-function SetLightIntensity(handle, intensity) end
-
----Lights that are owned by a dynamic shape are automatcially moved with that shape
----
---- ---
---- Example
----```lua
----local pos = GetLightTransform(light).pos
----```
----@param handle number
----@return table transform
-function GetLightTransform(handle) end
-
----No Description
----
---- ---
---- Example
----```lua
----local shape = GetLightShape(light)
----```
----@param handle number
----@return number handle
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
----@param handle number
----@return boolean active
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
----@param handle number
----@param point table
----@return boolean affected
-function IsPointAffectedByLight(handle, point) end
-
----No Description
----
---- ---
---- Example
----```lua
----local goal = FindTrigger("goal")
----```
----@param tag string
----@param global boolean
----@return number handle
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
----@param tag string
----@param global boolean
----@return table list
-function FindTriggers(tag, global) end
-
----No Description
----
---- ---
---- Example
----```lua
----local t = GetTriggerTransform(trigger)
----```
----@param handle number
----@return table transform
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
----@param handle number
----@param transform table
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
----@param handle number
----@return table min
----@return table max
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
----@param trigger number
----@param body number
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
----@param trigger number
----@param vehicle number
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
----@param trigger number
----@param shape number
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
----@param trigger number
----@param point table
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
----@param handle number
----@param demolision boolean
----@return boolean empty
----@return table maxpoint
-function IsTriggerEmpty(handle, demolision) end
-
----No Description
----
---- ---
---- Example
----```lua
----local screen = FindTrigger("tv")
----```
----@param tag string
----@param global boolean
----@return number handle
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
----@param tag string
----@param global boolean
----@return table list
-function FindScreens(tag, global) end
-
----Enable or disable screen
----
---- ---
---- Example
----```lua
----SetScreenEnabled(screen, true)
----```
----@param screen number
----@param enabled boolean
-function SetScreenEnabled(screen, enabled) end
-
----No Description
----
---- ---
---- Example
----```lua
----local b = IsScreenEnabled(screen)
----```
----@param screen number
----@return boolean enabled
-function IsScreenEnabled(screen) end
-
----Return handle to the parent shape of a screen
----
---- ---
---- Example
----```lua
----local shape = GetScreenShape(screen)
----```
----@param screen number
----@return number shape
-function GetScreenShape(screen) end
-
----No Description
----
---- ---
---- Example
----```lua
----local vehicle = FindVehicle("mycar")
----```
----@param tag string
----@param global boolean
----@return number handle
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
----@param tag string
----@param global boolean
----@return table list
-function FindVehicles(tag, global) end
-
----No Description
----
---- ---
---- Example
----```lua
----local t = GetVehicleTransform(vehicle)
----```
----@param vehicle number
----@return table transform
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
----@param vehicle number
----@return number body
-function GetVehicleBody(vehicle) end
-
----No Description
----
---- ---
---- Example
----```lua
----local health = GetVehicleHealth(vehicle)
----```
----@param vehicle number
----@return number health
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
----@param vehicle number
----@return table pos
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
----@param vehicle number
----@param drive number
----@param steering number
----@param handbrake boolean
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
----@return table position
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
----@param includePitch boolean
----@return table transform
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
----@param transform table
----@param includePitch boolean
-function SetPlayerTransform(transform, includePitch) end
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
----@return table transform
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
----@param transform table
-function SetPlayerSpawnTransform(transform) end
-
----No Description
----
---- ---
---- Example
----```lua
----local vel = GetPlayerVelocity()
----```
----@return table velocity
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
----@param vehicle number
-function SetPlayerVehicle(vehicle) end
-
----No Description
----
---- ---
---- Example
----```lua
----SetPlayerVelocity(Vec(0, 5, 0))
----```
----@param velocity table
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
----@return number handle
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
----@return number handle
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
----@return number handle
-function GetPlayerGrabBody() end
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
----@return number handle
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
----@return number handle
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
----@return number handle
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
----@return number handle
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
----@param handle number
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
----@return number handle
-function GetPlayerScreen() end
-
----No Description
----
---- ---
---- Example
----```lua
----SetPlayerHealth(0.5)
----```
----@param health number
-function SetPlayerHealth(health) end
-
----No Description
----
---- ---
---- Example
----```lua
----local health = GetPlayerHealth()
----```
----@return number health
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
----@param id string
----@param name string
----@param file string
----@param group number
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
----@return number handle
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
----@param transform table
----@param sway number
-function SetToolTransform(transform, sway) end
-
----No Description
----
---- ---
---- Example
----```lua
----local snd = LoadSound("beep.ogg")
----```
----@param path string
----@return number handle
-function LoadSound(path) end
-
----No Description
----
---- ---
---- Example
----```lua
----local loop = LoadLoop("siren.ogg")
----```
----@param path string
----@return number handle
-function LoadLoop(path) end
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
----@param handle number
----@param pos table
----@param volume number
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
----@param handle number
----@param pos table
----@param volume number
-function PlayLoop(handle, pos, volume) end
-
----No Description
----
---- ---
---- Example
----```lua
----PlayMusic("MOD/music/background.ogg")
----```
----@param path string
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
----@param path string
----@return number handle
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
----@param handle number
----@param transform table
----@param width number
----@param height number
----@param r number
----@param g number
----@param b number
----@param a number
----@param depthTest boolean
----@param additive boolean
-function DrawSprite(handle, transform, width, height, r, g, b, a, depthTest,
+nction SetValue(variable, value, transition, time) end
+
+nction PauseMenuButton(title) end
+
+nction StartLevel(mission, path, layers) end
+
+nction SetPaused(paused) end
+
+nction Restart() end
+
+nction Menu() end
+
+nction ClearKey(key) end
+
+nction ListKeys(parent) end
+
+nction HasKey(key) end
+
+nction SetInt(key, value, true) end
+
+nction GetInt(key) end
+
+nction SetFloat(key, value, true) end
+
+nction GetFloat(key) end
+
+nction SetBool(key, value, true) end
+
+nction GetBool(key) end
+
+nction SetString(key, value, true) end
+
+nction GetString(key) end
+
+nction Vec(x, y, z) end
+
+nction VecCopy(org) end
+
+nction VecLength(vec) end
+
+nction VecNormalize(vec) end
+
+nction VecScale(vec, scale) end
+
+nction VecAdd(a, b) end
+
+nction VecSub(a, b) end
+
+nction VecDot(a, b) end
+
+nction VecCross(a, b) end
+
+nction VecLerp(a, b, t) end
+
+nction Quat(x, y, z, w) end
+
+nction QuatCopy(org) end
+
+nction QuatAxisAngle(axis, angle) end
+
+nction QuatEuler(x, y, z) end
+
+nction GetQuatEuler(quat) end
+
+nction QuatLookAt(eye, target) end
+
+nction QuatSlerp(a, b, t) end
+
+nction QuatRotateQuat(a, b) end
+
+nction Transform(pos, rot) end
+
+nction TransformCopy(org) end
+
+nction TransformToParentTransform(parent, child) end
+
+nction TransformToLocalTransform(parent, child) end
+
+nction TransformToParentVec(t, v) end
+
+nction TransformToLocalVec(t, v) end
+
+nction TransformToParentPoint(t, p) end
+
+nction TransformToLocalPoint(t, p) end
+
+nction SetTag(handle, tag, value) end
+
+nction RemoveTag(handle, tag) end
+
+nction HasTag(handle, tag) end
+
+nction GetTagValue(handle, tag) end
+
+nction GetDescription(handle) end
+
+nction SetDescription(handle, description) end
+
+nction Delete(handle) end
+
+nction IsHandleValid(handle) end
+
+nction FindBody(tag, global) end
+
+nction FindBodies(tag, global) end
+
+nction GetBodyTransform(handle) end
+
+nction SetBodyTransform(handle, transform) end
+
+nction GetBodyMass(handle) end
+
+nction IsBodyDynamic(handle) end
+
+nction SetBodyDynamic(handle, dynamic) end
+
+nction SetBodyVelocity(handle, velocity) end
+
+nction GetBodyVelocity(handle) end
+
+nction GetBodyVelocityAtPos(handle, pos) end
+
+nction SetBodyAngularVelocity(handle, angVel) end
+
+nction GetBodyAngularVelocity(handle) end
+
+nction IsBodyActive(handle) end
+
+nction ApplyBodyImpulse(handle, position, impulse) end
+
+nction GetBodyShapes(handle) end
+
+nction GetBodyVehicle(body) end
+
+nction GetBodyBounds(handle) end
+
+nction GetBodyCenterOfMass(handle) end
+
+nction IsBodyVisible(handle, maxDist, rejectTransparent) end
+
+nction IsBodyBroken(handle) end
+
+nction IsBodyJointedToStatic(handle) end
+
+nction DrawBodyOutline(handle, r, g, b, a) end
+
+nction DrawBodyHighlight(handle, amount) end
+
+nction FindShape(tag, global) end
+
+nction FindShapes(tag, global) end
+
+nction GetShapeLocalTransform(handle) end
+
+nction SetShapeLocalTransform(handle, transform) end
+
+nction GetShapeWorldTransform(handle) end
+
+nction GetShapeBody(handle) end
+
+nction GetShapeJoints(shape) end
+
+nction GetShapeLights(shape) end
+
+nction GetShapeBounds(handle) end
+
+nction SetShapeEmissiveScale(handle, scale) end
+
+nction GetShapeMaterialAtPosition(handle, pos) end
+
+nction GetShapeMaterialAtIndex(handle, x, y, z) end
+
+nction GetShapeClosestPoint(shape, origin, maxDist) end
+
+nction GetShapeSize(handle) end
+
+nction GetShapeVoxelCount(handle) end
+
+nction IsShapeVisible(handle, maxDist, rejectTransparent) end
+
+nction IsShapeBroken(handle) end
+
+nction DrawShapeOutline(handle, r, g, b, a) end
+
+nction DrawShapeHighlight(handle, amount) end
+
+nction FindLocation(tag, global) end
+
+nction FindLocations(tag, global) end
+
+nction GetLocationTransform(handle) end
+
+nction FindJoint(tag, global) end
+
+nction FindJoints(tag, global) end
+
+nction IsJointBroken(joint) end
+
+nction GetJointType(joint) end
+
+nction GetJointOtherShape(joint, shape) end
+
+nction SetJointMotor(joint, velocity, strength) end
+
+nction SetJointMotorTarget(joint, target, maxVel, strength) end
+
+nction GetJointLimits(joint) end
+
+nction GetJointMovement(joint) end
+
+nction FindLight(tag, global) end
+
+nction FindLights(tag, global) end
+
+nction SetLightEnabled(handle, enabled) end
+
+nction SetLightColor(handle, r, g, b) end
+
+nction SetLightIntensity(handle, intensity) end
+
+nction GetLightTransform(handle) end
+
+nction GetLightShape(handle) end
+
+nction IsLightActive(handle) end
+
+nction IsPointAffectedByLight(handle, point) end
+
+nction FindTrigger(tag, global) end
+
+nction FindTriggers(tag, global) end
+
+nction GetTriggerTransform(handle) end
+
+nction SetTriggerTransform(handle, transform) end
+
+nction GetTriggerBounds(handle) end
+
+nction IsBodyInTrigger(trigger, body) end
+
+nction IsVehicleInTrigger(trigger, vehicle) end
+
+nction IsShapeInTrigger(trigger, shape) end
+
+nction IsPointInTrigger(trigger, point) end
+
+nction IsTriggerEmpty(handle, demolision) end
+
+nction FindScreen(tag, global) end
+
+nction FindScreens(tag, global) end
+
+nction SetScreenEnabled(screen, enabled) end
+
+nction IsScreenEnabled(screen) end
+
+nction GetScreenShape(screen) end
+
+nction FindVehicle(tag, global) end
+
+nction FindVehicles(tag, global) end
+
+nction GetVehicleTransform(vehicle) end
+
+nction GetVehicleBody(vehicle) end
+
+nction GetVehicleHealth(vehicle) end
+
+nction GetVehicleDriverPos(vehicle) end
+
+nction DriveVehicle(vehicle, drive, steering, handbrake) end
+
+nction GetPlayerPos(playerId) end
+
+nction GetPlayerTransform(playerId, includePitch) end
+
+nction SetPlayerTransform(playerId, transform, includePitch) end
+
+nction GetPlayerCameraTransform(playerId) end
+
+nction SetPlayerSpawnTransform(transform) end
+
+nction GetPlayerVelocity(playerId) end
+
+nction SetPlayerVehicle(playerId, vehicle) end
+
+nction SetPlayerVelocity(playerId, velocity) end
+
+nction GetPlayerVehicle(playerId) end
+
+nction GetPlayerGrabShape(playerId) end
+
+nction GetPlayerGrabBody(playerId) end
+
+nction GetPlayerPickShape(playerId) end
+
+nction GetPlayerPickBody(playerId) end
+
+nction GetPlayerInteractShape(playerId) end
+
+nction GetPlayerInteractBody(playerId) end
+
+nction SetPlayerScreen(handle) end
+
+nction GetPlayerScreen() end
+
+nction SetPlayerHealth(playerId, health) end
+
+nction GetPlayerHealth(playerId) end
+
+nction RespawnPlayer(playerId) end
+
+nction RegisterTool(id, name, file, group) end
+
+nction GetToolBody() end
+
+nction SetToolTransform(transform, sway) end
+
+nction LoadSound(path) end
+
+nction LoadLoop(path) end
+
+nction PlaySound(handle, pos, volume) end
+
+nction PlayLoop(handle, pos, volume) end
+
+nction PlayMusic(path) end
+
+nction StopMusic() end
+
+nction LoadSprite(path) end
+
+nction DrawSprite(handle, transform, width, height, r, g, b, a, depthTest,
                     additive) end
 
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
----QueryRaycast(...)
----```
----@param layers string
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
----@param vehicle number
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
----@param body number
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
----@param shape number
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
----@param origin table
----@param direction table
----@param maxDist number
----@param radius number
----@param rejectTransparent boolean
----@return boolean hit
----@return number dist
----@return table normal
----@return number shape
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
----local hit, p, n, s = QueryClosestPoint(Vec(0, 5, 0), 10)
----if hit then
----	--Point p of shape s is closest
----end
----```
----@param origin table
----@param maxDist number
----@return boolean hit
----@return table point
----@return table normal
----@return number shape
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
----@param min table
----@param max table
----@return table list
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
----@param min table
----@param max table
----@return table list
-function QueryAabbBodies(min, max) end
-
----No Description
----
---- ---
---- Example
----```lua
----local vol, pos = GetLastSound()
----```
----@return number volume
----@return table position
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
----@param point table
----@return boolean inWater
----@return number depth
-function IsPointInWater(point) end
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
----@param type string
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
----@param type integer
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
----@param r0 number
----@param g0 number
----@param b0 number
----@param r1 number
----@param g1 number
----@param b1 number
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
----@param r0 number
----@param r1 number
----@param interpolation string
----@param fadein number
----@param fadeout number
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
----@param a0 number
----@param a1 number
----@param interpolation string
----@param fadein number
----@param fadeout number
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
----@param g0 number
----@param g1 number
----@param interpolation string
----@param fadein number
----@param fadeout number
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
----@param d0 number
----@param d1 number
----@param interpolation string
----@param fadein number
----@param fadeout number
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
----@param d0 number
----@param d1 number
----@param interpolation string
----@param fadein number
----@param fadeout number
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
----@param r0 number
----@param r1 number
----@param interpolation string
----@param fadein number
----@param fadeout number
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
----@param s0 number
----@param s1 number
----@param interpolation string
----@param fadein number
----@param fadeout number
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
----@param s0 number
----@param s1 number
----@param interpolation string
----@param fadein number
----@param fadeout number
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
----@param c0 number
----@param c1 number
----@param interpolation string
----@param fadein number
----@param fadeout number
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
----@param bitmask number
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
----@param pos table
----@param velocity table
----@param lifetime number
-function SpawnParticle(pos, velocity, lifetime) end
-
----Shoot bullet or rocket (used for chopper)
----
---- ---
---- Example
----```lua
----Shoot(Vec(0, 10, 0), Vec(0, 0, 1))
----```
----@param origin table
----@param direction table
----@param type number
-function Shoot(origin, direction, type) end
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
----@param position table
----@param r0 number
----@param r1 number
----@param r2 number
----@param silent boolean
-function MakeHole(position, r0, r1, r2, silent) end
-
----No Description
----
---- ---
---- Example
----```lua
----Explosion(Vec(0, 10, 0), 1)
----```
----@param pos table
----@param size number
-function Explosion(pos, size) end
-
----No Description
----
---- ---
---- Example
----```lua
----SpawnFire(Vec(0, 10, 0))
----```
----@param pos table
-function SpawnFire(pos) end
-
----No Description
----
---- ---
---- Example
----```lua
----local c = GetFireCount()
----```
----@return number count
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
----@param origin table
----@param maxDist number
----@return boolean hit
----@return table pos
-function QueryClosestFire(origin, maxDist) end
-
----No Description
----
---- ---
---- Example
----```lua
----local count = QueryAabbFireCount(Vec(0,0,0), Vec(10,10,10))
----```
----@param min table
----@param max table
----@return number count
-function QueryAabbFireCount(min, max) end
-
----No Description
----
---- ---
---- Example
----```lua
----local removedCount= RemoveAabbFires(Vec(0,0,0), Vec(10,10,10))
----```
----@param min table
----@param max table
----@return number count
-function RemoveAabbFires(min, max) end
-
----No Description
----
---- ---
---- Example
----```lua
----local t = GetCameraTransform()
----```
----@return table transform
-function GetCameraTransform() end
-
----Override current camera transform for this frame. Call continuously to keep overriding.
----
---- ---
---- Example
----```lua
----SetCameraTransform(Transform(Vec(0, 10, 0), QuatEuler(0, 90, 0)))
----```
----@param transform table
----@param fov number
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
----@param float number
-function SetCameraFov(float) end
-
----Add a temporary point light to the world for this frame. Call continuously
----for a steady light.
----
---- ---
---- Example
----```lua
------Pulsating, yellow light above world origo
----local intensity = 3 + math.sin(GetTime())
----PointLight(Vec(0, 5, 0), 1, 1, 0, intensity)
----```
----@param pos table
----@param r number
----@param g number
----@param b number
----@param intensity number
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
----@param scale number
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
----exactly the same as in the editor.
----
---- ---
---- Example
----```lua
----SetEnvironmentProperty("skybox", "cloudy.dds")
----SetEnvironmentProperty("rain", 0.7)
----SetEnvironmentProperty("fogcolor", 0.5, 0.5, 0.8)
----SetEnvironmentProperty("nightlight", false)
----```
----@param name string
----@param value0 any
----@param value1 any
----@param value2 any
----@param value3 any
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
----@param name string
----@return any value0
----@return any value1
----@return any value2
----@return any value3
----@return any value4
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
----@param name string
----@param value0 number
----@param value1 number
----@param value2 number
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
----@param name string
----@return number value0
----@return number value1
----@return number value2
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
----@param p0 table
----@param p1 table
----@param r number
----@param g number
----@param b number
----@param a number
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
----@param p0 table
----@param p1 table
----@param r number
----@param g number
----@param b number
----@param a number
-function DebugLine(p0, p1, r, g, b, a) end
-
----Draw a debug cross in the world to highlight a location. Default color is white.
----
---- ---
---- Example
----```lua
----DebugCross(Vec(10, 5, 5))
----```
----@param p0 table
----@param r number
----@param g number
----@param b number
----@param a number
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
----@param name string
----@param value string
-function DebugWatch(name, value) end
-
----Display message on screen. The last 20 lines are displayed.
----
---- ---
---- Example
----```lua
----DebugPrint("time")
----```
----@param message string
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
----UiColor(1,0,0)
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
----@return number width
-function UiWidth() end
-
----No Description
----
---- ---
---- Example
----```lua
----local h = UiHeight()
----```
----@return number height
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
----@return number center
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
----@return number middle
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
----@param r number
----@param g number
----@param b number
----@param a number
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
----@param r number
----@param g number
----@param b number
----@param a number
-function UiColorFilter(r, g, b, a) end
-
----Translate cursor
----
---- ---
---- Example
----```lua
----UiPush()
----	UiTranslate(100, 0)
----	UiText("Indented")
----UiPop()
----```
----@param x number
----@param y number
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
----@param angle number
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
----@param x number
----@param y number
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
----@param width number
----@param height number
----@param clip boolean
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
----@return number x0
----@return number y0
----@return number x1
----@return number y1
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
----@param alignment string
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
----if UiButtonText("Okay") then
----	--Will never happen
----end
----
----UiEnableInput()
----if UiButtonText("Okay") then
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
----@return boolean receives
-function UiReceivesInput() end
-
----Get mouse pointer position relative to the cursor
----
---- ---
---- Example
----```lua
----local x, y = UiGetMousePos()
----```
----@return number x
----@return number y
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
----@param w number
----@param h number
----@return boolean inside
-function UiIsMouseInRect(w, h) end
-
----Convert world space position to user interface X and Y coordinate relative
----to the cursor. The distance is in meters and positive if in front of camera,
----negative otherwise.
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
----@param point table
----@return number x
----@return number y
----@return number distance
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
----@param x number
----@param y number
----@return table direction
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
----@param amount number
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
----@param path string
----@param size number
-function UiFont(path, size) end
-
----No Description
----
---- ---
---- Example
----```lua
----local h = UiFontHeight()
----```
----@return number size
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
----@param text string
----@param move boolean
----@return number w
----@return number h
-function UiText(text, move) end
-
----No Description
----
---- ---
---- Example
----```lua
----local w, h = UiGetTextSize("Some text")
----```
----@param text string
----@return number w
----@return number h
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
----@param width number
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
----@param r number
----@param g number
----@param b number
----@param a number
----@param thickness number
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
----@param r number
----@param g number
----@param b number
----@param a number
----@param distance number
----@param blur number
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
----@param w number
----@param h number
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
----@param path string
----@return number w
----@return number h
-function UiImage(path) end
-
----Get image size
----
---- ---
---- Example
----```lua
----local w,h = UiGetImageSize("test.png")
----```
----@param path string
----@return number w
----@return number h
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
----@param path string
----@param width number
----@param height number
----@param borderWidth number
----@param borderHeight number
-function UiImageBox(path, width, height, borderWidth, borderHeight) end
-
----UI sounds are not affected by acoustics simulation. Use LoadSound / PlaySound for that.
----
---- ---
---- Example
----```lua
----UiSound("click.ogg")
----```
----@param path string
----@param volume number
----@param pitch number
----@param pan number
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
----@param path string
----@param volume number
-function UiSoundLoop(path, volume) end
-
----Mute game audio and optionally music for the next frame. Call
----continuously to stay muted.
----
---- ---
---- Example
----```lua
----if menuOpen then
----	UiMute(1.0)
----end
----```
----@param amount number
----@param music boolean
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
----@param path string
----@param borderWidth number
----@param borderHeight number
----@param r number
----@param g number
----@param b number
----@param a number
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
----@param r number
----@param g number
----@param b number
----@param a number
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
----@param r number
----@param g number
----@param b number
----@param a number
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
----@param dist number
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
----@param text string
----@param w number
----@param h number
----@return boolean pressed
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
----@param path number
----@param w number
----@param h number
----@return boolean pressed
-function UiImageButton(path, w, h) end
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
----@param w number
----@param h number
----@return boolean pressed
-function UiBlankButton(w, h) end
-
----No Description
----
---- ---
---- Example
----```lua
----value = UiSlider("dot.png", "x", value, 0, 100)
----```
----@param path number
----@param axis string
----@param current number
----@param min number
----@param max number
----@return number value
----@return boolean done
-function UiSlider(path, axis, current, min, max) end
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
----@return number handle
-function UiGetScreen() end
+tion QueryRequire(layers) end
+
+--
+
+tion QueryRejectVehicle(vehicle) end
+
+--
+
+tion QueryRejectBody(body) end
+
+--
+
+tion QueryRejectShape(shape) end
+
+--
+
+tion QueryRaycast(origin, direction, maxDist, radius, rejectTransparent) end
+
+--
+
+tion QueryClosestPoint(origin, maxDist) end
+
+--
+
+tion QueryAabbShapes(min, max) end
+
+--
+
+tion QueryAabbBodies(min, max) end
+
+--
+
+tion GetLastSound() end
+
+--
+
+tion IsPointInWater(point) end
+
+--
+
+tion ParticleReset() end
+
+--
+
+tion ParticleType(type) end
+
+--
+
+tion ParticleTile(type) end
+
+--
+
+tion ParticleColor(r0, g0, b0, r1, g1, b1) end
+
+--
+
+tion ParticleRadius(r0, r1, interpolation, fadein, fadeout) end
+
+--
+
+tion ParticleAlpha(a0, a1, interpolation, fadein, fadeout) end
+
+--
+
+tion ParticleGravity(g0, g1, interpolation, fadein, fadeout) end
+
+--
+
+tion ParticleDrag(d0, d1, interpolation, fadein, fadeout) end
+
+--
+
+tion ParticleEmissive(d0, d1, interpolation, fadein, fadeout) end
+
+--
+
+tion ParticleRotation(r0, r1, interpolation, fadein, fadeout) end
+
+--
+
+tion ParticleStretch(s0, s1, interpolation, fadein, fadeout) end
+
+--
+
+tion ParticleSticky(s0, s1, interpolation, fadein, fadeout) end
+
+--
+
+tion ParticleCollide(c0, c1, interpolation, fadein, fadeout) end
+
+--
+
+tion ParticleFlags(bitmask) end
+
+--
+
+tion SpawnParticle(pos, velocity, lifetime) end
+
+--
+
+tion Shoot(origin, direction, type) end
+
+--
+
+tion MakeHole(position, r0, r1, r2, silent) end
+
+--
+
+tion Explosion(pos, size) end
+
+--
+
+tion SpawnFire(pos) end
+
+--
+
+tion GetFireCount() end
+
+--
+
+tion QueryClosestFire(origin, maxDist) end
+
+--
+
+tion QueryAabbFireCount(min, max) end
+
+--
+
+tion RemoveAabbFires(min, max) end
+
+--
+
+tion GetCameraTransform() end
+
+--
+
+tion SetCameraTransform(transform, fov) end
+
+--
+
+tion SetCameraFov(float) end
+
+--
+
+tion PointLight(pos, r, g, b, intensity) end
+
+--
+
+tion SetTimeScale(scale) end
+
+--
+
+tion SetEnvironmentDefault() end
+
+--
+
+tion SetEnvironmentProperty(name, value0, value1, value2, value3) end
+
+--
+
+tion GetEnvironmentProperty(name) end
+
+--
+
+tion SetPostProcessingDefault() end
+
+--
+
+tion SetPostProcessingProperty(name, value0, value1, value2) end
+
+--
+
+tion GetPostProcessingProperty(name) end
+
+--
+
+tion DrawLine(p0, p1, r, g, b, a) end
+
+--
+
+tion DebugLine(p0, p1, r, g, b, a) end
+
+--
+
+tion DebugCross(p0, r, g, b, a) end
+
+--
+
+tion DebugWatch(name, value) end
+
+--
+
+tion DebugPrint(message) end
+
+--
+
+tion UiMakeInteractive() end
+
+--
+
+tion UiPush() end
+
+--
+
+tion UiPop() end
+
+--
+
+tion UiWidth() end
+
+--
+
+tion UiHeight() end
+
+--
+
+tion UiCenter() end
+
+--
+
+tion UiMiddle() end
+
+--
+
+tion UiColor(r, g, b, a) end
+
+--
+
+tion UiColorFilter(r, g, b, a) end
+
+--
+
+tion UiTranslate(x, y) end
+
+--
+
+tion UiRotate(angle) end
+
+--
+
+tion UiScale(x, y) end
+
+--
+
+tion UiWindow(width, height, clip) end
+
+--
+
+tion UiSafeMargins() end
+
+--
+
+on UiAlign(alignment) end
+
+---D
+
+on UiModalBegin() end
+
+---D
+
+on UiModalEnd() end
+
+---D
+
+on UiDisableInput() end
+
+---E
+
+on UiEnableInput() end
+
+---T
+
+on UiReceivesInput() end
+
+---G
+
+on UiGetMousePos() end
+
+---C
+
+on UiIsMouseInRect(w, h) end
+
+---C
+
+on UiWorldToPixel(point) end
+
+---C
+
+on UiPixelToWorld(x, y) end
+
+---P
+
+on UiBlur(amount) end
+
+---N
+
+on UiFont(path, size) end
+
+---N
+
+on UiFontHeight() end
+
+---N
+
+on UiText(text, move) end
+
+---N
+
+on UiGetTextSize(text) end
+
+---N
+
+on UiWordWrap(width) end
+
+---N
+
+on UiTextOutline(r, g, b, a, thickness) end
+
+---N
+
+on UiTextShadow(r, g, b, a, distance, blur) end
+
+---D
+
+on UiRect(w, h) end
+
+---D
+
+on UiImage(path) end
+
+---G
+
+on UiGetImageSize(path) end
+
+---D
+
+on UiImageBox(path, width, height, borderWidth, borderHeight) end
+
+---U
+
+on UiSound(path, volume, pitch, pan) end
+
+---C
+
+on UiSoundLoop(path, volume) end
+
+---M
+
+on UiMute(amount, music) end
+
+---S
+
+on UiButtonImageBox(path, borderWidth, borderHeight, r, g, b, a) end
+
+---B
+
+on UiButtonHoverColor(r, g, b, a) end
+
+---B
+
+on UiButtonPressColor(r, g, b, a) end
+
+---T
+
+on UiButtonPressDist(dist) end
+
+---N
+
+on UiTextButton(text, w, h) end
+
+---N
+
+on UiImageButton(path, w, h) end
+
+---N
+
+on UiBlankButton(w, h) end
+
+---N
+
+on UiSlider(path, axis, current, min, max) end
+
+---N
+
+on UiGetScreen() end
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

# Migration Report: zombieMod\instances\contraptions\contraption_flamer.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/zombieMod\instances\contraptions\contraption_flamer.lua
+++ patched/zombieMod\instances\contraptions\contraption_flamer.lua
@@ -1,26 +1,4 @@
-function init()
-
-    nozzleShapes = FindShapes('nozzle')
-    base = FindShape('base')
-
-    playerDamageAmt = 0.02
-
-    timer = {
-        time = 0,
-        rpm = 400,
-    }
-
-    loops = {
-        nozzle = LoadLoop("tools/blowtorch-loop")
-    }
-
-
-end
-
-function tick()
-    runNozzles()
-end
-
+#version 2
 function runNozzles()
     for i = 1, #nozzleShapes do
 
@@ -29,12 +7,11 @@
         local nTr = GetShapeWorldTransform(nShape)
 
         -- Player properties.
-        local playerNearNozzle = VecDist(GetPlayerTransform().pos, nTr.pos) < 1.5
+        local playerNearNozzle = VecDist(GetPlayerTransform(playerId).pos, nTr.pos) < 1.5
 
         -- Center of nozzle shape.
         local nMin, nMax = GetShapeBounds(nShape)
         nTr.pos = VecLerp(nMin, nMax, 0.5)
-
 
         -- Raycast. Timed for performance.
         local rcTr = nil
@@ -50,7 +27,6 @@
             timer.time = timer.time - GetTimeStep()
         end
 
-
         -- Manage nozzle shooting.
         if (hit or playerNearNozzle) and rcTr ~= nil then
 
@@ -63,8 +39,8 @@
 
             -- Player hit by fire.
             if playerNearNozzle then
-                local playerHealthHit = GetPlayerHealth() - playerDamageAmt
-                SetPlayerHealth(playerHealthHit)
+                local playerHealthHit = GetPlayerHealth(playerId) - playerDamageAmt
+                SetPlayerHealth(playerId, playerHealthHit)
             end
 
             -- Spawn fire particle.
@@ -75,9 +51,6 @@
     end
 end
 
-
-
--- [[UTILITY]]
 function raycastFromTransform(tr, distance, rad, rejectBody)
     local plyTransform = tr
     local fwdPos = TransformToParentPoint(plyTransform, Vec(0, 0, -distance or -300))
@@ -92,4 +65,25 @@
     end
     return nil
 end
-function VecDist(vec1, vec2) return VecLength(VecSub(vec1, vec2)) end+
+function VecDist(vec1, vec2) return VecLength(VecSub(vec1, vec2)) end
+
+function server.init()
+    nozzleShapes = FindShapes('nozzle')
+    base = FindShape('base')
+    playerDamageAmt = 0.02
+    timer = {
+        time = 0,
+        rpm = 400,
+    }
+    loops = {
+        nozzle = LoadLoop("tools/blowtorch-loop")
+    }
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        runNozzles()
+    end
+end
+

```

---

# Migration Report: zombieMod\instances\contraptions\contraption_mace.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/zombieMod\instances\contraptions\contraption_mace.lua
+++ patched/zombieMod\instances\contraptions\contraption_mace.lua
@@ -1,10 +1,18 @@
-function init()
+#version 2
+function server.init()
     maceHeadJoint = FindJoint('maceHeadJoint')
     maceHeadShape = FindShape('maceHead')
     maceLoop = LoadLoop('MOD/zombieMod/instances/contraptions/sounds/maceLoop.ogg')
 end
 
-function tick()
-    SetJointMotor(maceHeadJoint, 30, 1000000)
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        SetJointMotor(maceHeadJoint, 30, 1000000)
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
     PlayLoop(maceLoop, GetShapeWorldTransform(maceHeadShape).pos, 2)
 end
+

```

---

# Migration Report: zombieMod\main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/zombieMod\main.lua
+++ patched/zombieMod\main.lua
@@ -1,234 +1 @@
-#include "scripts/utility.lua"
-#include "scripts/zombie.lua"
-#include "scripts/zombieRadar.lua"
-#include "scripts/info.lua"
-#include "scripts/customWeapons.lua"
--- #include "mods/C Glock/main.lua"
--- #include 'mods/C M4A1/main.lua'
--- #include 'mods/C P90/main.lua'
-
-
--- ================================================================
--- Zombie AI - by: Cheejins
--- ================================================================
-
--- ----------------------------------------------------------------
--- This script ties together all of the other scripts.
--- ----------------------------------------------------------------
-
-
-
---[[INIT]]
-function init()
-
-    initOptionsMain()
-    initGame()
-    initMap()
-    initBoids()
-
-    initZombies() -- Init zombies last after all other values are set.
-    initZombieController()
-
-    -- initGlock18()
-    -- initM4A1()
-    -- initP90()
-
-
-end
-
-
-
---[[TICK]]
-function tick()
-
-    -- Game..
-    updateGameTable()
-
-    -- Custom Weapons
-    -- runGlock18()
-    -- runM4A1()
-    -- runP90()
-
-    -- Zombies..
-    manageZombies()
-    manageMapTriggers()
-    runZombieController()
-    runZombieRadar()
-
-    -- Map.
-    -- disableTools()
-
-    -- Debug.
-    -- debugMod()
-
-end
-
-function draw()
-    UiPush()
-        runZombieRadar()
-    UiPop()
-
-    UiPush()
-        drawInfoUi()
-    UiPop()
-end
-
-
---[[DEBUG]]
-function debugMod()
-    -- DebugWatch('#zombiesTable', #zombiesTable)
-    for i = 1, #zombiesTable do
-        local zombie = zombiesTable[i]
-        -- DebugWatch("Zombie"..zombie.id.." state", zombie.ai.state)
-    end
-end
-function debugZombie(zombie)
-    local zTr = zombie:getTr()
-    local fwdZ = Vec(0,0,-25)
-    local revZ = Vec(0,0,25)
-    local fwdPos = TransformToParentPoint(zTr, fwdZ)
-    local revPos = TransformToParentPoint(zTr, revZ)
-    -- DebugLine(zTr.pos, fwdPos, 1,1,0)
-    -- DebugLine(zTr.pos, revPos, 1,1,0)
-end
-
-
-
---[[GAME]]
-function updateGameTable()
-    game.ppos = VecAdd(GetPlayerPos(), Vec(0,1,0))
-    game.playerAabb.min = VecAdd(game.ppos, Vec(game.playerAabb.minAdd))
-    game.playerAabb.max = VecAdd(game.ppos, Vec(game.playerAabb.maxAdd))
-end
-function initGame()
-    colors = getColors()
-
-    game = {
-        playerPos = GetPlayerPos(),
-        playerAabb = {
-            minAdd = Vec(-2,0,-2),
-            maxAdd = Vec(2,2,2),
-            min = Vec(-2,0,-2),
-            max = Vec(2,2,2),
-        },
-    }
-
-    sounds = {
-        deaths = {
-            LoadSound("MOD/zombieMod/snd/deaths/death1.ogg"),
-        },
-
-        hits = {
-            LoadSound("MOD/zombieMod/snd/hits/hits1.ogg"),
-            LoadSound("MOD/zombieMod/snd/hits/hits2.ogg"),
-            LoadSound("MOD/zombieMod/snd/hits/hits3.ogg"),
-            LoadSound("MOD/zombieMod/snd/hits/hits4.ogg"),
-        },
-
-        growls = {
-            LoadSound("MOD/zombieMod/snd/growls/growl1.ogg"),
-            LoadSound("MOD/zombieMod/snd/growls/growl2.ogg"),
-            LoadSound("MOD/zombieMod/snd/growls/growl3.ogg"),
-            LoadSound("MOD/zombieMod/snd/growls/growl4.ogg"),
-        },
-
-        damage = {
-            LoadSound("MOD/zombieMod/snd/damage/damage1.ogg"),
-            LoadSound("MOD/zombieMod/snd/damage/damage2.ogg"),
-            LoadSound("MOD/zombieMod/snd/damage/damage3.ogg"),
-        }
-    }
-
-    sounds.play = {
-        damage = function (zombie, vol)
-            sounds.playRandom(zombie, sounds.damage, vol or 2)
-        end,
-
-        death = function(zombie, vol)
-            sounds.playRandom(zombie, sounds.deaths, vol or 1)
-        end,
-
-        growl = function (zombie, vol)
-            sounds.playRandom(zombie, sounds.growls, vol or 2)
-        end,
-
-        hit = function(zombie, vol)
-            sounds.playRandom(zombie, sounds.hits, vol or 1.5)
-        end,
-    }
-
-    sounds.playRandom = function(zombie, soundsTable, vol)
-        local p = math.floor(soundsTable[rdm(1, #soundsTable)])
-        PlaySound(p, zombie.getPos(), vol or 1)
-        -- DebugWatch('hit sound', p)
-    end
-
-end
-function initOptionsMain()
-    if GetBool('savegame.mod.options.init') == false then
-
-        SetString('savegame.mod.zombieRadar.corner', 'tr')
-        SetBool('savegame.mod.options.outline', true)
-        -- SetBool('savegame.mod.options.customWeapons', true)
-
-        SetBool('savegame.mod.options.init', true)
-    end
-end
-
-
---[[MAP]]
--- Zombies can be activated by triggers. Make sure the trigger has the tag trigger with a value of whatever you'd like. ex: trig=start, trig=forest
-function initMap()
-    SCRIPTED_MAP = false
-    map = {
-        triggers = {
-            refs = {},
-            names = {},
-            activated = {},
-        },
-    }
-    if FindLocation("ai_zombie_map", true) ~= 0 then
-        SCRIPTED_MAP = true
-        -- DebugPrint("Map is scripted ai zombie map...")
-        initTriggers()
-    end
-end
-function initTriggers()
-    map.triggers.refs = FindTriggers("trig", true)
-    for i = 1, #map.triggers.refs do
-
-        local trigger = map.triggers.refs[i]
-        local tagVal = GetTagValue(trigger, "trig")
-
-        map.triggers.names[tagVal] = tagVal
-        map.triggers.refs[tagVal] = trigger
-        map.triggers.activated[i] = 0
-
-        -- DebugPrint("activated: " .. map.triggers.activated[i])
-        -- DebugPrint("trigger: " .. map.triggers.names[tagVal])
-    end
-end
-function manageMapTriggers()
-    for i = 1, #map.triggers.refs do
-        if map.triggers.activated[i] == 0 then -- Activate trigger once only.
-            for j = 1, #zombiesTable do
-                if zombiesTable[j].ai.isActive == false then
-                    if IsBodyInTrigger(map.triggers.refs[i], zombiesTable[j].body) 
-                    and IsPointInTrigger(map.triggers.refs[i], game.ppos) then
-                        zombiesTable[j].ai.isActive = true -- Activate ai in trigger zone.
-                        map.triggers.activated[i] = 1 -- Activate trigger zone.
-                    end
-                end
-            end
-        end
-    end
-end
-function disableTools(pickedUpTools)
-    local toolNames = {sledge = 'sledge', spraycan = 'spraycan', extinguisher ='extinguisher', blowtorch = 'blowtorch'}
-    local tools = ListKeys("game.tool")
-    for i=1, #tools do
-        if tools[i] == toolNames[tools[i]] then
-            SetBool("game.tool."..tools[i]..".enabled", false)
-        end
-    end
-end+#version 2

```

---

# Migration Report: zombieMod\mods\C Glock\main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/zombieMod\mods\C Glock\main.lua
+++ patched/zombieMod\mods\C Glock\main.lua
@@ -1,32 +1,14 @@
+#version 2
 local damageStart = 0.175
-
 local TOOL = {}
-
-TOOL.printname = "Desert Eagle"
-TOOL.order = 2
-TOOL.base = "gun"
-
-TOOL.suppress_default = true
-
 local STATE_READY = 0
 local STATE_RELOADING = 2
 
-deagleprojectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {
-		active = false,
-		damage = damageStart,
-		shootPos = nil,
-	},
-}
-
-
 function initGlock18()
 
 	RegisterTool("z-glock18", "Z-Glock 18", "MOD/zombieMod/mods/C Glock/vox/glock.vox")
-	SetBool("game.tool.z-glock18.enabled", true)
-	SetFloat("game.tool.z-glock18.ammo", 101)
+	SetBool("game.tool.z-glock18.enabled", true, true)
+	SetFloat("game.tool.z-glock18.ammo", 101, true)
 
 	damage = damageStart
 	gravity = Vec(0, 0, 0)
@@ -39,7 +21,6 @@
 	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
 	maxDist = 25
 	diminishDamage = 0.9995
-
 
 	for i=1, ammo do
 		deagleprojectileHandler.shells[i] = deepcopy(deagleprojectileHandler.defaultShell)
@@ -106,7 +87,7 @@
 
 	SpawnParticle("fire", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.5, 0.1)
 	SpawnParticle("darksmoke", toolPos, Vec(0, 1.0+math.random(1,5)*0.1, 0), 0.4, 1.5)
-	PlaySound(gunsound, GetPlayerTransform().pos, 0.9, false)
+	PlaySound(gunsound, GetPlayerTransform(playerId).pos, 0.9, false)
 	if not unlimitedammo then
 		ammo = ammo - 1
 	end
@@ -145,21 +126,17 @@
 		return
 	end
 	reloading = true
-	PlaySound(reloadsound, GetPlayerTransform().pos, 0.6, false)
+	PlaySound(reloadsound, GetPlayerTransform(playerId).pos, 0.6, false)
 	reloadTimer = reloadTime
 	mags = mags - 1
 end
 
-function tick(dt)
-	runGlock18(dt)
-end
-
 function runGlock18(dt)
-	if GetString("game.player.tool") == "z-glock18" and GetPlayerVehicle() == 0 then
+	if GetString("game.player.tool") == "z-glock18" and GetPlayerVehicle(playerId) == 0 then
 		if InputPressed("lmb") then
 			if not reloading then
 				if mags == 0 or ammo == 0 then
-					PlaySound(dryfiresound, GetPlayerTransform().pos, 1, false)
+					PlaySound(dryfiresound, GetPlayerTransform(playerId).pos, 1, false)
 				else
 					Shoot()
 				end
@@ -173,7 +150,7 @@
 			toolTrans = GetBodyTransform(b)
 			toolPos = TransformToParentPoint(toolTrans, Vec(0.3, -0.45, -2.4))
 
-			if recoilTimer > 0 then
+			if recoilTimer ~= 0 then
 				local t = Transform()
 				t.pos = Vec(0.1, 0.1, recoilTimer*3)
 				t.rot = QuatEuler(recoilTimer*100, 0, 0)
@@ -182,7 +159,7 @@
 				recoilTimer = recoilTimer - dt
 			end
 
-			if lightTimer > 0 then
+			if lightTimer ~= 0 then
 				PointLight(toolPos, 1, 1, 1, 0.5)
 
 				lightTimer = lightTimer - dt
@@ -195,9 +172,9 @@
 			end
 			
 			if GetBool("ammobox.refill") then
-				SetBool("ammobox.refill", false)
+				SetBool("ammobox.refill", false, true)
 				mags = mags + 1
-				PlaySound(refillsound, GetPlayerTransform().pos, 1, false)
+				PlaySound(refillsound, GetPlayerTransform(playerId).pos, 1, false)
 			end
 
 			if reloading then
@@ -223,20 +200,27 @@
 	end
 end
 
-function draw()
-	if GetString("game.player.tool") == "z-glock18" and GetPlayerVehicle() == 0 and not unlimitedammo then
-		UiPush()
-			UiTranslate(UiCenter(), (UiCenter()/2) + 300)
-			UiAlign("center middle")
-			local c = ammo / #deagleprojectileHandler.shells
-			UiColor(1, c, c)
-			UiFont("bold.ttf", 24)
-			UiTextOutline(0,0,0,1,0.1)
-			if reloading then
-				UiText("Reloading")
-			else
-				UiText(ammo.."/"..18*math.max(0, mags-1))
-			end
-		UiPop()
-	end
-end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        runGlock18(dt)
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "z-glock18" and GetPlayerVehicle(playerId) == 0 and not unlimitedammo then
+    	UiPush()
+    		UiTranslate(UiCenter(), (UiCenter()/2) + 300)
+    		UiAlign("center middle")
+    		local c = ammo / #deagleprojectileHandler.shells
+    		UiColor(1, c, c)
+    		UiFont("bold.ttf", 24)
+    		UiTextOutline(0,0,0,1,0.1)
+    		if reloading then
+    			UiText("Reloading")
+    		else
+    			UiText(ammo.."/"..18*math.max(0, mags-1))
+    		end
+    	UiPop()
+    end
+end
+

```

---

# Migration Report: zombieMod\mods\C Glock\options.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/zombieMod\mods\C Glock\options.lua
+++ patched/zombieMod\mods\C Glock\options.lua
@@ -1,42 +1,4 @@
-function init()
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-	if unlimitedammo == 0 then unlimitedammo = 0.15 end
-end
-
-function draw()
-	UiTranslate(UiCenter(), 350)
-	UiAlign("center middle")
-
-	UiFont("bold.ttf", 48)
-	UiText("Desert Eagle")
-	UiFont("regular.ttf", 26)
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("Unlimited Ammo")
-		UiTranslate(15, 40)
-		UiAlign("right")
-		UiColor(0.5, 0.8, 1)
-		if unlimitedammo then
-			if UiTextButton("Yes", 20, 20) then
-				unlimitedammo = false
-				SetBool("savegame.mod.unlimitedammo", unlimitedammo)
-			end
-		else
-			if UiTextButton("No", 20, 20) then
-				unlimitedammo = true
-				SetBool("savegame.mod.unlimitedammo", unlimitedammo)
-			end
-		end
-	UiPop()
-
-	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-
-	UiTranslate(0, 120)
-	if UiTextButton("Close", 80, 40) then
-		Menu()
-	end
-end
-
+#version 2
 function optionsSlider(val, min, max)
 	UiColor(0.2, 0.6, 1)
 	UiPush()
@@ -55,4 +17,44 @@
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    if unlimitedammo == 0 then unlimitedammo = 0.15 end
+end
+
+function client.draw()
+    UiTranslate(UiCenter(), 350)
+    UiAlign("center middle")
+
+    UiFont("bold.ttf", 48)
+    UiText("Desert Eagle")
+    UiFont("regular.ttf", 26)
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("Unlimited Ammo")
+    	UiTranslate(15, 40)
+    	UiAlign("right")
+    	UiColor(0.5, 0.8, 1)
+    	if unlimitedammo then
+    		if UiTextButton("Yes", 20, 20) then
+    			unlimitedammo = false
+    			SetBool("savegame.mod.unlimitedammo", unlimitedammo, true)
+    		end
+    	else
+    		if UiTextButton("No", 20, 20) then
+    			unlimitedammo = true
+    			SetBool("savegame.mod.unlimitedammo", unlimitedammo, true)
+    		end
+    	end
+    UiPop()
+
+    UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+
+    UiTranslate(0, 120)
+    if UiTextButton("Close", 80, 40) then
+    	Menu()
+    end
+end
+

```

---

# Migration Report: zombieMod\mods\C M4A1\main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/zombieMod\mods\C M4A1\main.lua
+++ patched/zombieMod\mods\C M4A1\main.lua
@@ -1,53 +1,5 @@
+#version 2
 local damageStart = 0.25
-
-
-m4a1projectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {
-		active = false,
-		damage = damageStart,
-		shootPos = nil,
-	},
-}
-
-function init()
-	RegisterTool("z-m4a1", "Z-M4A1", "MOD/zombieMod/mods/C M4A1/vox/m4a1.vox")
-	SetBool("game.tool.z-m4a1.enabled", true)
-	SetFloat("game.tool.z-m4a1.ammo", 101)
-
-	gravity = Vec(0, 0, 0)
-	velocity = 4
-
-	gunsound = LoadSound("MOD/zombieMod/mods/C M4A1/snd/m4.ogg")
-	cocksound = LoadSound("MOD/zombieMod/mods/C M4A1/snd/guncock.ogg")
-	reloadsound = LoadSound("MOD/zombieMod/mods/C M4A1/snd/reload.ogg")
-	dryfiresound = LoadSound("MOD/zombieMod/mods/C M4A1/snd/dryfire.ogg")
-	refillsound = LoadSound("MOD/zombieMod/mods/C M4A1/snd/refill.ogg")
-
-	reloadTime = 2
-	shotDelay = 0.13
-	spreadTimer = 0
-	ammo = 25
-	mags = 50
-	reloading = false
-	ironsight = false
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-	maxDist = 50
-	diminishDamage = 0.9999
-	for i=1, ammo do
-		m4a1projectileHandler.shells[i] = deepcopy(m4a1projectileHandler.defaultShell)
-		m4a1projectileHandler.shells[i].shootPos = toolPos
-	end
-
-	shootTimer = 0
-	reloadTimer = 0
-	recoilTimer = 0
-	lightTimer = 0
-
-	magoutTimer = 0
-	maginTimer = 0
-end
 
 function deepcopy(orig)
     local orig_type = type(orig)
@@ -87,7 +39,7 @@
 
 	local p = toolPos
 	local dir = VecSub(aimpos, p)
-	local plVel = VecLength(GetPlayerVelocity())
+	local plVel = VecLength(GetPlayerVelocity(playerId))
 	local maxSpread = InputDown("ctrl") and 1.5 or 3 * ((plVel*4) + 1)
 	if ironsight then maxSpread = maxSpread / 2 end
 	local spread = math.min(spreadTimer, maxSpread) * distance/100
@@ -104,7 +56,7 @@
 	m4a1projectileHandler.shellNum = (m4a1projectileHandler.shellNum%#m4a1projectileHandler.shells) + 1
 
 	SpawnParticle("fire", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.1)
-	PlaySound(gunsound, GetPlayerTransform().pos, 1, false)
+	PlaySound(gunsound, GetPlayerTransform(playerId).pos, 1, false)
 
 	if not unlimitedammo then
 		ammo = ammo - 1
@@ -134,7 +86,6 @@
 	projectile.pos = point2
 	projectile.damage = projectile.damage * diminishDamage
 
-
 	if VecLength(VecSub(projectile.pos, projectile.shootPos)) > maxDist then
 		projectile.active = false
 	end
@@ -145,148 +96,186 @@
 		return
 	end
 	reloading = true
-	PlaySound(reloadsound, GetPlayerTransform().pos, 0.6, false)
+	PlaySound(reloadsound, GetPlayerTransform(playerId).pos, 0.6, false)
 	reloadTimer = reloadTime
 	magoutTimer = 0.6
 	mags = mags - 1
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "z-m4a1" and GetPlayerVehicle() == 0 then
-		if InputDown("lmb") and ammo > 0 and not reloading then
-			Shoot()
-		end
-
-		if InputPressed("lmb") and not reloading then
-			spreadTimer = 0
-			if ammo == 0 then
-				PlaySound(dryfiresound, GetPlayerTransform().pos, 1, false)
-			end
-		end
-
-		if InputReleased("lmb") and ammo > 0 then
-			SpawnParticle("darksmoke", gunpos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.5)
-		end
-
-		if InputPressed("rmb") then
-			ironsight = not ironsight
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local heightOffset = InputDown("ctrl") and 0.25 or 0.2
-			local magoffset = Vec(0, 0, 0)
-			local magtimer = magoutTimer + maginTimer
-			local offset = Transform(Vec(0, heightOffset, 0))
-			local x, y, z, rot = 0, heightOffset, 0, 0
-			if ironsight then
-				x = 0.32
-				y = 0.355
-				z = 0.3
-				rot = 2.5
-				offset = Transform(Vec(-x, y, z), QuatEuler(-rot, 0, 0))
-			end
-
-			if magtimer > 0 then
-				offset.rot = QuatEuler(10, 0, -10)
-				offset.pos = VecAdd(offset.pos, Vec(0.2, 0.2, 0))
-				magoffset = Vec(-0.6, -0.6, 0.6)
-			end
-
-			SetToolTransform(offset)
-			toolTrans = GetBodyTransform(b)
-			toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.6, -2.35))
-
-			if recoilTimer > 0 then
-				local t = Transform()
-				t.pos = Vec(-x, y, recoilTimer+z)
-				ironrot = ironsight and rot or -recoilTimer*50-rot
-				t.rot = QuatEuler(-ironrot, 0, 0)
-				SetToolTransform(t)
-
-				recoilTimer = recoilTimer - dt
-			end
-
-			if lightTimer > 0 then
-				PointLight(toolPos, 1, 1, 1, 0.5)
-				lightTimer = lightTimer - dt
-			end
-			
-			if magoutTimer > 0 then
-				magoffset = Vec(-0.3+magoutTimer/2, -0.6+magoutTimer, 0.9-magoutTimer*1.5)
-				magoutTimer = magoutTimer - dt
-				if magoutTimer < 0 then
-					maginTimer = 0.6
-				end
-			end
-
-			if maginTimer > 0 then
-				magoffset = Vec(-maginTimer/2, -maginTimer, maginTimer*1.5)
-				maginTimer = maginTimer - dt
-			end
-			
-			if body ~= b then
-				body = b
-				local shapes = GetBodyShapes(b)
-				mag = shapes[2]
-				magTrans = GetShapeLocalTransform(mag)
-			end
-
-			mt = TransformCopy(magTrans)
-			mt.pos = VecAdd(mt.pos, magoffset)
-			mt.rot = QuatRotateQuat(mt.rot, QuatEuler(-magtimer*30, magtimer*30, 0))
-			SetShapeLocalTransform(mag, mt)
-		end
-
-		if not unlimitedammo then
-			if ammo < 30 and mags > 1 and InputPressed("R") then
-				Reload()
-			end
-			
-			if GetBool("ammobox.refill") then
-				SetBool("ammobox.refill", false)
-				mags = mags + 1
-				PlaySound(refillsound, GetPlayerTransform().pos, 1, false)
-			end
-
-			if reloading then
-				ironsight = false
-				reloadTimer = reloadTimer - dt
-				if reloadTimer < 0 then
-					ammo = 30
-					reloadTimer = 0
-					PlaySound(cocksound)
-					reloading = false
-				end
-			end
-		end
-
-		for key, shell in ipairs(m4a1projectileHandler.shells) do
-			if shell.active then
-				ProjectileOperations(shell)
-			end
-		end
-	
-		if shootTimer > 0 or ammo == 0 then
-			shootTimer = shootTimer - dt
-		end
-	end
-end
-
-function draw()
-	if GetString("game.player.tool") == "z-m4a1" and GetPlayerVehicle() == 0 and not unlimitedammo then
-		UiPush()
-			UiTranslate(UiCenter(), (UiCenter()/2) + 300)
-			UiAlign("center middle")
-			local c = ammo / #m4a1projectileHandler.shells
-			UiColor(1, c, c)
-			UiFont("bold.ttf", 24)
-			UiTextOutline(0,0,0,1,0.1)
-			if reloading then
-				UiText("Reloading")
-			else
-				UiText(ammo.."/"..30*math.max(0, mags-1))
-			end
-		UiPop()
-	end
-end+function server.init()
+    RegisterTool("z-m4a1", "Z-M4A1", "MOD/zombieMod/mods/C M4A1/vox/m4a1.vox")
+    SetBool("game.tool.z-m4a1.enabled", true, true)
+    SetFloat("game.tool.z-m4a1.ammo", 101, true)
+    gravity = Vec(0, 0, 0)
+    velocity = 4
+    reloadTime = 2
+    shotDelay = 0.13
+    spreadTimer = 0
+    ammo = 25
+    mags = 50
+    reloading = false
+    ironsight = false
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    maxDist = 50
+    diminishDamage = 0.9999
+    for i=1, ammo do
+    	m4a1projectileHandler.shells[i] = deepcopy(m4a1projectileHandler.defaultShell)
+    	m4a1projectileHandler.shells[i].shootPos = toolPos
+    end
+    shootTimer = 0
+    reloadTimer = 0
+    recoilTimer = 0
+    lightTimer = 0
+    magoutTimer = 0
+    maginTimer = 0
+end
+
+function client.init()
+    gunsound = LoadSound("MOD/zombieMod/mods/C M4A1/snd/m4.ogg")
+    cocksound = LoadSound("MOD/zombieMod/mods/C M4A1/snd/guncock.ogg")
+    reloadsound = LoadSound("MOD/zombieMod/mods/C M4A1/snd/reload.ogg")
+    dryfiresound = LoadSound("MOD/zombieMod/mods/C M4A1/snd/dryfire.ogg")
+    refillsound = LoadSound("MOD/zombieMod/mods/C M4A1/snd/refill.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "z-m4a1" and GetPlayerVehicle(playerId) == 0 then
+    	if InputDown("lmb") and ammo > 0 and not reloading then
+    		Shoot()
+    	end
+
+    	if InputPressed("lmb") and not reloading then
+    		spreadTimer = 0
+    		if ammo == 0 then
+    			PlaySound(dryfiresound, GetPlayerTransform(playerId).pos, 1, false)
+    		end
+    	end
+
+    	if InputReleased("lmb") and ammo ~= 0 then
+    		SpawnParticle("darksmoke", gunpos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.5)
+    	end
+
+    	if InputPressed("rmb") then
+    		ironsight = not ironsight
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local heightOffset = InputDown("ctrl") and 0.25 or 0.2
+    		local magoffset = Vec(0, 0, 0)
+    		local magtimer = magoutTimer + maginTimer
+    		local offset = Transform(Vec(0, heightOffset, 0))
+    		local x, y, z, rot = 0, heightOffset, 0, 0
+    		if ironsight then
+    			x = 0.32
+    			y = 0.355
+    			z = 0.3
+    			rot = 2.5
+    			offset = Transform(Vec(-x, y, z), QuatEuler(-rot, 0, 0))
+    		end
+
+    		if magtimer ~= 0 then
+    			offset.rot = QuatEuler(10, 0, -10)
+    			offset.pos = VecAdd(offset.pos, Vec(0.2, 0.2, 0))
+    			magoffset = Vec(-0.6, -0.6, 0.6)
+    		end
+
+    		SetToolTransform(offset)
+    		toolTrans = GetBodyTransform(b)
+    		toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.6, -2.35))
+
+    		if recoilTimer ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(-x, y, recoilTimer+z)
+    			ironrot = ironsight and rot or -recoilTimer*50-rot
+    			t.rot = QuatEuler(-ironrot, 0, 0)
+    			SetToolTransform(t)
+
+    			recoilTimer = recoilTimer - dt
+    		end
+
+    		if lightTimer ~= 0 then
+    			PointLight(toolPos, 1, 1, 1, 0.5)
+    			lightTimer = lightTimer - dt
+    		end
+
+    		if magoutTimer ~= 0 then
+    			magoffset = Vec(-0.3+magoutTimer/2, -0.6+magoutTimer, 0.9-magoutTimer*1.5)
+    			magoutTimer = magoutTimer - dt
+    			if magoutTimer < 0 then
+    				maginTimer = 0.6
+    			end
+    		end
+
+    		if maginTimer ~= 0 then
+    			magoffset = Vec(-maginTimer/2, -maginTimer, maginTimer*1.5)
+    			maginTimer = maginTimer - dt
+    		end
+
+    		if body ~= b then
+    			body = b
+    			local shapes = GetBodyShapes(b)
+    			mag = shapes[2]
+    			magTrans = GetShapeLocalTransform(mag)
+    		end
+
+    		mt = TransformCopy(magTrans)
+    		mt.pos = VecAdd(mt.pos, magoffset)
+    		mt.rot = QuatRotateQuat(mt.rot, QuatEuler(-magtimer*30, magtimer*30, 0))
+    		SetShapeLocalTransform(mag, mt)
+    	end
+
+    	if not unlimitedammo then
+    		if ammo < 30 and mags > 1 and InputPressed("R") then
+    			Reload()
+    		end
+
+    		if GetBool("ammobox.refill") then
+    			SetBool("ammobox.refill", false, true)
+    			mags = mags + 1
+    			PlaySound(refillsound, GetPlayerTransform(playerId).pos, 1, false)
+    		end
+
+    		if reloading then
+    			ironsight = false
+    			reloadTimer = reloadTimer - dt
+    			if reloadTimer < 0 then
+    				ammo = 30
+    				reloadTimer = 0
+    				PlaySound(cocksound)
+    				reloading = false
+    			end
+    		end
+    	end
+
+    	for key, shell in ipairs(m4a1projectileHandler.shells) do
+    		if shell.active then
+    			ProjectileOperations(shell)
+    		end
+    	end
+
+    	if shootTimer > 0 or ammo == 0 then
+    		shootTimer = shootTimer - dt
+    	end
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "z-m4a1" and GetPlayerVehicle(playerId) == 0 and not unlimitedammo then
+    	UiPush()
+    		UiTranslate(UiCenter(), (UiCenter()/2) + 300)
+    		UiAlign("center middle")
+    		local c = ammo / #m4a1projectileHandler.shells
+    		UiColor(1, c, c)
+    		UiFont("bold.ttf", 24)
+    		UiTextOutline(0,0,0,1,0.1)
+    		if reloading then
+    			UiText("Reloading")
+    		else
+    			UiText(ammo.."/"..30*math.max(0, mags-1))
+    		end
+    	UiPop()
+    end
+end
+

```

---

# Migration Report: zombieMod\mods\C M4A1\options.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/zombieMod\mods\C M4A1\options.lua
+++ patched/zombieMod\mods\C M4A1\options.lua
@@ -1,42 +1,4 @@
-function init()
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-	if unlimitedammo == 0 then unlimitedammo = 0.15 end
-end
-
-function draw()
-	UiTranslate(UiCenter(), 350)
-	UiAlign("center middle")
-
-	UiFont("bold.ttf", 48)
-	UiText("M4A1")
-	UiFont("regular.ttf", 26)
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("Unlimited Ammo")
-		UiTranslate(15, 40)
-		UiAlign("right")
-		UiColor(0.5, 0.8, 1)
-		if unlimitedammo then
-			if UiTextButton("Yes", 20, 20) then
-				unlimitedammo = false
-				SetBool("savegame.mod.unlimitedammo", unlimitedammo)
-			end
-		else
-			if UiTextButton("No", 20, 20) then
-				unlimitedammo = true
-				SetBool("savegame.mod.unlimitedammo", unlimitedammo)
-			end
-		end
-	UiPop()
-
-	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-
-	UiTranslate(0, 120)
-	if UiTextButton("Close", 80, 40) then
-		Menu()
-	end
-end
-
+#version 2
 function optionsSlider(val, min, max)
 	UiColor(0.2, 0.6, 1)
 	UiPush()
@@ -55,4 +17,44 @@
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    if unlimitedammo == 0 then unlimitedammo = 0.15 end
+end
+
+function client.draw()
+    UiTranslate(UiCenter(), 350)
+    UiAlign("center middle")
+
+    UiFont("bold.ttf", 48)
+    UiText("M4A1")
+    UiFont("regular.ttf", 26)
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("Unlimited Ammo")
+    	UiTranslate(15, 40)
+    	UiAlign("right")
+    	UiColor(0.5, 0.8, 1)
+    	if unlimitedammo then
+    		if UiTextButton("Yes", 20, 20) then
+    			unlimitedammo = false
+    			SetBool("savegame.mod.unlimitedammo", unlimitedammo, true)
+    		end
+    	else
+    		if UiTextButton("No", 20, 20) then
+    			unlimitedammo = true
+    			SetBool("savegame.mod.unlimitedammo", unlimitedammo, true)
+    		end
+    	end
+    UiPop()
+
+    UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+
+    UiTranslate(0, 120)
+    if UiTextButton("Close", 80, 40) then
+    	Menu()
+    end
+end
+

```

---

# Migration Report: zombieMod\mods\C P90\main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/zombieMod\mods\C P90\main.lua
+++ patched/zombieMod\mods\C P90\main.lua
@@ -1,50 +1,5 @@
+#version 2
 local damageStart = 0.15
-
-p90projectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {
-		active = false,
-		damage = damageStart,
-		shootPos = nil,
-	},
-}
-
-function init()
-	RegisterTool("p90", "P90", "MOD/zombieMod/mods/C P90/vox/p90.vox")
-	SetBool("game.tool.p90.enabled", true)
-	SetFloat("game.tool.p90.ammo", 101)
-
-	damage = damageStart
-	gravity = Vec(0, 0, 0)
-	velocity = 3
-
-	gunsound = LoadSound("MOD/zombieMod/mods/C P90/snd/p90.ogg")
-	cocksound = LoadSound("MOD/zombieMod/mods/C P90/snd/p90cock.ogg")
-	reloadsound = LoadSound("MOD/zombieMod/mods/C P90/snd/p90reload.ogg")
-	dryfiresound = LoadSound("MOD/zombieMod/mods/C P90/snd/dryfire.ogg")
-	refillsound = LoadSound("MOD/zombieMod/mods/C P90/snd/refill.ogg")
-
-	reloadTime = 2
-	shotDelay = 0.06
-	spreadTimer = 0
-	ammo = 50
-	mags = 50
-	reloading = false
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-	maxDist = 50
-	diminishDamage = 0.99
-
-	for i=1, ammo do
-		p90projectileHandler.shells[i] = deepcopy(p90projectileHandler.defaultShell)
-		p90projectileHandler.shells[i].shootPos = toolPos
-	end
-
-	shootTimer = 0
-	reloadTimer = 0
-	recoilTimer = 0
-	lightTimer = 0
-end
 
 function deepcopy(orig)
     local orig_type = type(orig)
@@ -100,7 +55,7 @@
 	p90projectileHandler.shellNum = (p90projectileHandler.shellNum%#p90projectileHandler.shells) + 1
 
 	SpawnParticle("fire", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.1)
-	PlaySound(gunsound, GetPlayerTransform().pos, 1, false)
+	PlaySound(gunsound, GetPlayerTransform(playerId).pos, 1, false)
 
 	if not unlimitedammo then
 		ammo = ammo - 1
@@ -142,100 +97,136 @@
 		return
 	end
 	reloading = true
-	PlaySound(reloadsound, GetPlayerTransform().pos, 0.6, false)
+	PlaySound(reloadsound, GetPlayerTransform(playerId).pos, 0.6, false)
 	reloadTimer = reloadTime
 	mags = mags - 1
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "p90" and GetPlayerVehicle() == 0 then
-		if InputDown("lmb") and ammo > 0 and not reloading then
-			Shoot()
-		end
-
-		if InputPressed("lmb") and not reloading then
-			spreadTimer = 0
-			if ammo == 0 then
-				PlaySound(dryfiresound, GetPlayerTransform().pos, 1, false)
-			end
-		end
-
-		if InputReleased("lmb") and ammo > 0 then
-			SpawnParticle("darksmoke", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.5)
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local heightOffset = InputDown("ctrl") and 0.3 or 0.2
-			local offset = Transform(Vec(0, heightOffset, 0))
-			SetToolTransform(offset)
-			toolTrans = GetBodyTransform(b)
-			toolPos = TransformToParentPoint(toolTrans, Vec(0.3, -0.5, -1.45))
-
-			if recoilTimer > 0 then
-				local t = Transform()
-				t.pos = Vec(0, heightOffset, recoilTimer)
-				t.rot = QuatEuler(recoilTimer*50, 0, 0)
-				SetToolTransform(t)
-
-				recoilTimer = recoilTimer - dt
-			end
-
-			if lightTimer > 0 then
-				PointLight(toolPos, 1, 1, 1, 0.5)
-
-				lightTimer = lightTimer - dt
-			end
-		end
-
-		if not unlimitedammo then
-			if ammo < 50 and mags > 1 and InputPressed("R") then
-				Reload()
-			end
-			
-			if GetBool("ammobox.refill") then
-				SetBool("ammobox.refill", false)
-				mags = mags + 1
-				PlaySound(refillsound, GetPlayerTransform().pos, 1, false)
-			end
-
-			if reloading then
-				reloadTimer = reloadTimer - dt
-				if reloadTimer < 0 then
-					ammo = 50
-					reloadTimer = 0
-					PlaySound(cocksound)
-					reloading = false
-				end
-			end
-		end
-
-		for key, shell in ipairs(p90projectileHandler.shells) do
-			if shell.active then
-				ProjectileOperations(shell)
-			end
-		end
-	
-		if shootTimer > 0 or ammo == 0 then
-			shootTimer = shootTimer - dt
-		end
-	end
-end
-
-function draw()
-	if GetString("game.player.tool") == "p90" and GetPlayerVehicle() == 0 and not unlimitedammo then
-		UiPush()
-			UiTranslate(UiCenter(), (UiCenter()/2) + 300)
-			UiAlign("center middle")
-			local c = ammo / #p90projectileHandler.shells
-			UiColor(1, c, c)
-			UiFont("bold.ttf", 24)
-			UiTextOutline(0,0,0,1,0.1)
-			if reloading then
-				UiText("Reloading")
-			else
-				UiText(ammo.."/"..50*math.max(0, mags-1))
-			end
-		UiPop()
-	end
-end+function server.init()
+    RegisterTool("p90", "P90", "MOD/zombieMod/mods/C P90/vox/p90.vox")
+    SetBool("game.tool.p90.enabled", true, true)
+    SetFloat("game.tool.p90.ammo", 101, true)
+    damage = damageStart
+    gravity = Vec(0, 0, 0)
+    velocity = 3
+    reloadTime = 2
+    shotDelay = 0.06
+    spreadTimer = 0
+    ammo = 50
+    mags = 50
+    reloading = false
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    maxDist = 50
+    diminishDamage = 0.99
+    for i=1, ammo do
+    	p90projectileHandler.shells[i] = deepcopy(p90projectileHandler.defaultShell)
+    	p90projectileHandler.shells[i].shootPos = toolPos
+    end
+    shootTimer = 0
+    reloadTimer = 0
+    recoilTimer = 0
+    lightTimer = 0
+end
+
+function client.init()
+    gunsound = LoadSound("MOD/zombieMod/mods/C P90/snd/p90.ogg")
+    cocksound = LoadSound("MOD/zombieMod/mods/C P90/snd/p90cock.ogg")
+    reloadsound = LoadSound("MOD/zombieMod/mods/C P90/snd/p90reload.ogg")
+    dryfiresound = LoadSound("MOD/zombieMod/mods/C P90/snd/dryfire.ogg")
+    refillsound = LoadSound("MOD/zombieMod/mods/C P90/snd/refill.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "p90" and GetPlayerVehicle(playerId) == 0 then
+    	if InputDown("lmb") and ammo > 0 and not reloading then
+    		Shoot()
+    	end
+
+    	if InputPressed("lmb") and not reloading then
+    		spreadTimer = 0
+    		if ammo == 0 then
+    			PlaySound(dryfiresound, GetPlayerTransform(playerId).pos, 1, false)
+    		end
+    	end
+
+    	if InputReleased("lmb") and ammo ~= 0 then
+    		SpawnParticle("darksmoke", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.5)
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local heightOffset = InputDown("ctrl") and 0.3 or 0.2
+    		local offset = Transform(Vec(0, heightOffset, 0))
+    		SetToolTransform(offset)
+    		toolTrans = GetBodyTransform(b)
+    		toolPos = TransformToParentPoint(toolTrans, Vec(0.3, -0.5, -1.45))
+
+    		if recoilTimer ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(0, heightOffset, recoilTimer)
+    			t.rot = QuatEuler(recoilTimer*50, 0, 0)
+    			SetToolTransform(t)
+
+    			recoilTimer = recoilTimer - dt
+    		end
+
+    		if lightTimer ~= 0 then
+    			PointLight(toolPos, 1, 1, 1, 0.5)
+
+    			lightTimer = lightTimer - dt
+    		end
+    	end
+
+    	if not unlimitedammo then
+    		if ammo < 50 and mags > 1 and InputPressed("R") then
+    			Reload()
+    		end
+
+    		if GetBool("ammobox.refill") then
+    			SetBool("ammobox.refill", false, true)
+    			mags = mags + 1
+    			PlaySound(refillsound, GetPlayerTransform(playerId).pos, 1, false)
+    		end
+
+    		if reloading then
+    			reloadTimer = reloadTimer - dt
+    			if reloadTimer < 0 then
+    				ammo = 50
+    				reloadTimer = 0
+    				PlaySound(cocksound)
+    				reloading = false
+    			end
+    		end
+    	end
+
+    	for key, shell in ipairs(p90projectileHandler.shells) do
+    		if shell.active then
+    			ProjectileOperations(shell)
+    		end
+    	end
+
+    	if shootTimer > 0 or ammo == 0 then
+    		shootTimer = shootTimer - dt
+    	end
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "p90" and GetPlayerVehicle(playerId) == 0 and not unlimitedammo then
+    	UiPush()
+    		UiTranslate(UiCenter(), (UiCenter()/2) + 300)
+    		UiAlign("center middle")
+    		local c = ammo / #p90projectileHandler.shells
+    		UiColor(1, c, c)
+    		UiFont("bold.ttf", 24)
+    		UiTextOutline(0,0,0,1,0.1)
+    		if reloading then
+    			UiText("Reloading")
+    		else
+    			UiText(ammo.."/"..50*math.max(0, mags-1))
+    		end
+    	UiPop()
+    end
+end
+

```

---

# Migration Report: zombieMod\mods\C P90\options.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/zombieMod\mods\C P90\options.lua
+++ patched/zombieMod\mods\C P90\options.lua
@@ -1,42 +1,4 @@
-function init()
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-	if unlimitedammo == 0 then unlimitedammo = 0.15 end
-end
-
-function draw()
-	UiTranslate(UiCenter(), 350)
-	UiAlign("center middle")
-
-	UiFont("bold.ttf", 48)
-	UiText("P90")
-	UiFont("regular.ttf", 26)
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("Unlimited Ammo")
-		UiTranslate(15, 40)
-		UiAlign("right")
-		UiColor(0.5, 0.8, 1)
-		if unlimitedammo then
-			if UiTextButton("Yes", 20, 20) then
-				unlimitedammo = false
-				SetBool("savegame.mod.unlimitedammo", unlimitedammo)
-			end
-		else
-			if UiTextButton("No", 20, 20) then
-				unlimitedammo = true
-				SetBool("savegame.mod.unlimitedammo", unlimitedammo)
-			end
-		end
-	UiPop()
-
-	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-
-	UiTranslate(0, 120)
-	if UiTextButton("Close", 80, 40) then
-		Menu()
-	end
-end
-
+#version 2
 function optionsSlider(val, min, max)
 	UiColor(0.2, 0.6, 1)
 	UiPush()
@@ -55,4 +17,44 @@
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    if unlimitedammo == 0 then unlimitedammo = 0.15 end
+end
+
+function client.draw()
+    UiTranslate(UiCenter(), 350)
+    UiAlign("center middle")
+
+    UiFont("bold.ttf", 48)
+    UiText("P90")
+    UiFont("regular.ttf", 26)
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("Unlimited Ammo")
+    	UiTranslate(15, 40)
+    	UiAlign("right")
+    	UiColor(0.5, 0.8, 1)
+    	if unlimitedammo then
+    		if UiTextButton("Yes", 20, 20) then
+    			unlimitedammo = false
+    			SetBool("savegame.mod.unlimitedammo", unlimitedammo, true)
+    		end
+    	else
+    		if UiTextButton("No", 20, 20) then
+    			unlimitedammo = true
+    			SetBool("savegame.mod.unlimitedammo", unlimitedammo, true)
+    		end
+    	end
+    UiPop()
+
+    UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+
+    UiTranslate(0, 120)
+    if UiTextButton("Close", 80, 40) then
+    	Menu()
+    end
+end
+

```

---

# Migration Report: zombieMod\options.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/zombieMod\options.lua
+++ patched/zombieMod\options.lua
@@ -1,53 +1,14 @@
+#version 2
 local ui = {}
-
-function init()
-    ui = {
-
-        text = {
-            size = {
-                s = 12,
-                m = 24,
-                l = 48,
-            },
-        },
-
-        container = {
-            width = 1440,
-            height = 240,
-            margin = 240,
-        },
-
-        padding = {
-            container = {
-                width = UiWidth() * 0.2,
-                height = UiHeight() * 0.1,
-            },
-        },
-
-        bgColor = 0.12,
-        fgColor = 0.4,
-    }
-end
-
-
-function draw()
-    initOptions()
-
-    UiPush()
-        drawHeader()
-        drawOptions()
-        drawCloseButton()
-    UiPop()
-end
 
 function initOptions()
     if GetBool('savegame.mod.options.init') == false then
 
-        SetString('savegame.mod.zombieRadar.corner', 'tr')
-        SetBool('savegame.mod.options.outline', true)
-        -- SetBool('savegame.mod.options.customWeapons', true)
-
-        SetBool('savegame.mod.options.init', true)
+        SetString('savegame.mod.zombieRadar.corner', 'tr', true)
+        SetBool('savegame.mod.options.outline', true, true)
+        -- SetBool('savegame.mod.options.customWeapons', true, true)
+
+        SetBool('savegame.mod.options.init', true, true)
     end
 end
 
@@ -139,14 +100,14 @@
             UiButtonImageBox("ui/common/box-solid-6.png", 10, 10, ui.fgColor,ui.fgColor,ui.fgColor)
 
             -- if GetString('savegame.mod.zombieRadar.corner') == '' then
-            --     SetString('savegame.mod.zombieRadar.corner','tl')
+            --     SetString('savegame.mod.zombieRadar.corner','tl', true)
             -- end
             UiPush()
                 if GetString('savegame.mod.zombieRadar.corner') == 'tl' then activeButton() end
                 UiTranslate(corners[1], 0)
 
                 if UiTextButton('Top Left', buttonW, buttonH) then
-                    SetString('savegame.mod.zombieRadar.corner','tl')
+                    SetString('savegame.mod.zombieRadar.corner','tl', true)
                 end
             UiPop()
             UiPush()
@@ -154,7 +115,7 @@
                 UiTranslate(corners[2], 0)
 
                 if UiTextButton('Top Right', buttonW, buttonH) then
-                    SetString('savegame.mod.zombieRadar.corner','tr')
+                    SetString('savegame.mod.zombieRadar.corner','tr', true)
                 end
             UiPop()
             UiPush()
@@ -162,7 +123,7 @@
                 UiTranslate(corners[3], 0)
 
                 if UiTextButton('Bottom Left', buttonW, buttonH) then
-                    SetString('savegame.mod.zombieRadar.corner','bl')
+                    SetString('savegame.mod.zombieRadar.corner','bl', true)
                 end
             UiPop()
             UiPush()
@@ -170,7 +131,7 @@
                 UiTranslate(corners[4], 0)
 
                 if UiTextButton('Bottom Right', buttonW, buttonH) then
-                    SetString('savegame.mod.zombieRadar.corner','br')
+                    SetString('savegame.mod.zombieRadar.corner','br', true)
                 end
             UiPop()
             UiPush()
@@ -178,11 +139,10 @@
                 UiTranslate(corners[5], 0)
 
                 if UiTextButton('OFF', buttonW, buttonH) then
-                    SetString('savegame.mod.zombieRadar.corner','off')
-                end
-            UiPop()
-        UiPop()
-
+                    SetString('savegame.mod.zombieRadar.corner','off', true)
+                end
+            UiPop()
+        UiPop()
 
         --[[MISC]]
         UiTranslate(0, ui.text.size.l*3)
@@ -204,7 +164,7 @@
                 end
 
                 if UiTextButton('Zombie Outline = ' .. toggleText, buttonW*2, buttonH) then
-                    SetBool('savegame.mod.options.outline', not GetBool('savegame.mod.options.outline'))
+                    SetBool('savegame.mod.options.outline', not GetBool('savegame.mod.options.outline'), true)
                 end
 
             UiPop()
@@ -227,7 +187,7 @@
         --         end
 
         --         if UiTextButton('Custom Weapons = ' .. toggleText, buttonW*2.2, buttonH) then
-        --             SetBool('savegame.mod.options.customWeapons', not GetBool('savegame.mod.options.customWeapons'))
+        --             SetBool('savegame.mod.options.customWeapons', not GetBool('savegame.mod.options.customWeapons'), true)
         --         end
         --     UiPop()
         -- UiPop()
@@ -249,3 +209,41 @@
     UiPop()
 end
 
+function server.init()
+    ui = {
+        text = {
+            size = {
+                s = 12,
+                m = 24,
+                l = 48,
+            },
+        },
+        container = {
+            width = 1440,
+            height = 240,
+            margin = 240,
+        },
+        padding = {
+            container = {
+            },
+        },
+        bgColor = 0.12,
+        fgColor = 0.4,
+    }
+end
+
+function client.init()
+    width = UiWidth() * 0.2,
+    height = UiHeight() * 0.1,
+end
+
+function client.draw()
+    initOptions()
+
+    UiPush()
+        drawHeader()
+        drawOptions()
+        drawCloseButton()
+    UiPop()
+end
+

```

---

# Migration Report: zombieMod\scripts\boids.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/zombieMod\scripts\boids.lua
+++ patched/zombieMod\scripts\boids.lua
@@ -1,14 +1,4 @@
-#include "utility.lua"
-
--- ====================================================================================================
--- Zombie AI - by: Cheejins
--- ====================================================================================================
-
--- ----------------------------------------------------------------------------------------------------
--- This script handles the boid navigation for zombies.
--- ----------------------------------------------------------------------------------------------------
-
-
+#version 2
 function initBoids()
 
     boidsData = {
@@ -44,7 +34,6 @@
     boidObstacles = {}
 end
 
-
 function computeAlignment(boid, boids)
 
     local boidTr = GetBodyTransform(boid)
@@ -83,7 +72,6 @@
     return VecScale(vel, boidsData.strength.align)
 end
 
-
 function computeCohesion(boid, boids)
 
     local boidTr = GetBodyTransform(boid)
@@ -118,7 +106,6 @@
     return VecScale(vel, boidsData.strength.cohesion)
 end
 
-
 function computeSeparation(boid, boids, targetPos, scale)
 
     scale = scale or 1
@@ -156,7 +143,6 @@
 
     return VecScale(vel, boidsData.strength.separation * scale)
 end
-
 
 function computeObstacles(boid)
 
@@ -192,13 +178,11 @@
     return VecScale(vel, boidsData.strength.obstacle)
 end
 
-
 function processBoids()
     populateObstacles()
     -- displayObstacles()
     boidsData.timer.time = boidsData.timer.time - GetTimeStep()
 end
-
 
 function populateObstacles()
     if boidsData.obstacles.initDone == false then
@@ -213,9 +197,9 @@
     boidsData.obstacles.initDone = true
 end
 
-
 function displayObstacles()
     for i = 1, #boidsData.obstacles.positions do
         DebugLine(boidsData.obstacles.positions[i], VecAdd(boidsData.obstacles.positions[i], Vec(0,5,0)), 1, 0, 0)
     end
 end
+

```

---

# Migration Report: zombieMod\scripts\customWeapons.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/zombieMod\scripts\customWeapons.lua
+++ patched/zombieMod\scripts\customWeapons.lua
@@ -0,0 +1 @@
+#version 2

```

---

# Migration Report: zombieMod\scripts\info.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/zombieMod\scripts\info.lua
+++ patched/zombieMod\scripts\info.lua
@@ -1,3 +1,4 @@
+#version 2
 local menu = {
     isShowing = false,
 }
@@ -17,4 +18,5 @@
     --     UiImageBox('MOD/zombieMod/img/info.png', 1449, 877, 1, 1)
     -- end
 
-end+end
+

```

---

# Migration Report: zombieMod\scripts\utility.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/zombieMod\scripts\utility.lua
+++ patched/zombieMod\scripts\utility.lua
@@ -1,11 +1,18 @@
---[[VECTORS]]
+#version 2
+local debugSounds = {
+    beep = LoadSound("warning-beep"),
+    buzz = LoadSound("light/spark0"),
+    chime = LoadSound("elevator-chime"),}
+
 function CalcDist(vec1, vec2)
     return VecLength(VecSub(vec1, vec2))
 end
+
 function VecDiv(v, n)
     n = n or 1
     return Vec(v[1] / n, v[2] / n, v[3] / n)
 end
+
 function VecAddAll(vectorsTable)
     local v = Vec(0,0,0)
     for i = 1, #vectorsTable do
@@ -13,11 +20,11 @@
     end
     return v
 end
---- return number if not = 0, else return 0.00000001
+
 function VecRdm(min, max)
     return Vec(rdm(min, max),rdm(min, max),rdm(min, max))
 end
---- Prints quats or vectors. dec = decimal places. dec default = 3. title is optional.
+
 function printVec(vec, dec, title)
     DebugPrint(
         (title or "") .. 
@@ -26,7 +33,7 @@
         "  " .. sfn(vec[3], dec or 2)
     )
 end
---- Fully prints quats or vectors will all decimals. title is optional.
+
 function printVecf(vec, title)
     DebugPrint(
         (title or "") .. 
@@ -35,6 +42,7 @@
         "  " .. sfn(vec[3])
     )
 end
+
 function particleLine(vec1, vec2, particle, density, thickness)
     local maxLength = 500 -- prevents infinite particle line crashing your game.
     local transform = Transform(vec1, QuatLookAt(vec1,vec2))
@@ -46,16 +54,10 @@
     end
 end
 
-
-
---[[QUAT]]
 function QuatLookDown(pos)
     return QuatLookAt(pos, VecAdd(pos, Vec(0, -1, 0)))
 end
 
-
-
---[[AABB]]
 function drawAabb(v1, v2, r, g, b, a)
     r = r or 1
     g = g or 1
@@ -85,12 +87,14 @@
     DebugLine(Vec(x1,y1,z2), Vec(x1,y1,z1), r, g, b, a)
     DebugLine(Vec(x1,y2,z2), Vec(x1,y2,z1), r, g, b, a)
 end
+
 function checkAabbOverlap(aMin, aMax, bMin, bMax)
     return 
     (aMin[1] <= bMax[1] and aMax[1] >= bMin[1]) and
     (aMin[2] <= bMax[2] and aMax[2] >= bMin[2]) and
     (aMin[3] <= bMax[3] and aMax[3] >= bMin[3])
 end
+
 function aabbClosestEdge(pos, shape)
 
     local shapeAabbMin, shapeAabbMax = GetShapeBounds(shape)
@@ -116,7 +120,7 @@
     end
     return closestEdge, index
 end
---- Sort edges by closest to startPos and closest to endPos. Return sorted table.
+
 function sortAabbEdges(startPos, endPos, edges)
 
     local s, startIndex = aabbClosestEdge(startPos, edges)
@@ -129,16 +133,12 @@
     return edges
 end
 
-
-
---[[TABLES]]
 function tableSwapIndex(t, i1, i2)
     local temp = t[i1]
     t[i1] = t[i2]
     t[i2] = temp
     return t
 end
-
 
 function raycastFromTransform(tr, distance, rad, rejectBody)
 
@@ -163,6 +163,7 @@
         return nil
     end
 end
+
 function diminishBodyAngVel(body, rate)
     local angVel = GetBodyAngularVelocity(body)
     local dRate = rate or 0.99
@@ -170,8 +171,6 @@
     SetBodyAngularVelocity(body, diminishedAngVel)
 end
 
-
---[[VFX]]
 function getColors()
     local colors = {
         white = Vec(1,1,1),
@@ -194,62 +193,39 @@
     DrawSprite(dot, spriteTr, 0.2, 0.2, r or 1, g or 1, b or 1, 1)
 end
 
-
-
---[[SFX]]
-local debugSounds = {
-    beep = LoadSound("warning-beep"),
-    buzz = LoadSound("light/spark0"),
-    chime = LoadSound("elevator-chime"),}
-function beep(vol) PlaySound(debugSounds.beep, GetPlayerPos(), vol or 0.3) end
-function buzz(vol) PlaySound(debugSounds.buzz, GetPlayerPos(), vol or 0.3) end
-function chime(vol) PlaySound(debugSounds.chime, GetPlayerPos(), vol or 0.3) end
-
--- ---comment
--- ---@param path string Path to the folder of sounds.
--- ---@param baseWord string String of the sound without numbers. Ex: for sounds hit1, hit2, hit3, the base word is hit.
--- ---@return table
--- function GetAllSoundsFromFolder(path, baseWord)
---     local sounds = {}
---     local i = 1
---     while path..baseWord..tostring(i) ~= nil do
---         sounds[i] = 
---         i = i+1
---     end
---     return sounds
--- end
-
-
-
---[[MATH]]
+function beep(vol) PlaySound(debugSounds.beep, GetPlayerPos(playerId), vol or 0.3) end
+
+function buzz(vol) PlaySound(debugSounds.buzz, GetPlayerPos(playerId), vol or 0.3) end
+
+function chime(vol) PlaySound(debugSounds.chime, GetPlayerPos(playerId), vol or 0.3) end
+
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
 end
---- return number if > 0, else return 0.00000001
+
 function gtZero(val)
     if val <= 0 then
         return 0.0000001
     end
     return val
 end
---- return number if not = 0, else return 0.00000001
+
 function nZero(val)
     if val == 0 then return 0.0000001 end
     return val
 end
---- return number if not = 0, else return 0.00000001
+
 function rdm(min, max)
     return math.random(min or 0, max or 1)
 end
 
-
---[[FORMATTING]]
---- string format. default 2 decimals.
 function sfn(numberToFormat, dec)
     local s = (tostring(dec or 2))
     return string.format("%."..s.."f", numberToFormat)
 end
+
 function sfnTime(dec)
     return sfn(' '..GetTime(), dec or 4)
-end+end
+

```

---

# Migration Report: zombieMod\scripts\zombie.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/zombieMod\scripts\zombie.lua
+++ patched/zombieMod\scripts\zombie.lua
@@ -1,294 +1,4 @@
-#include "scripts/boids.lua"
-#include "scripts/utility.lua"
-#include "scripts/zombieController.lua"
-#include "scripts/zombieConstructor.lua"
-
-
--- ====================================================================================================
--- Zombie AI - by: Cheejins
--- ====================================================================================================
-
--- ----------------------------------------------------------------------------------------------------
--- This script handles the movement, actions and AI of the zombie.
--- ----------------------------------------------------------------------------------------------------
-
-zombiesTable = {}
-
-
-function initZombies()
-    local zombieBodies = FindBodies("ai_zombie", true)
-    for i = 1, #zombieBodies do -- Store body references.
-        local body = zombieBodies[i]
-        local zombie = createZombie(body, i)
-        table.insert(zombiesTable, zombie)
-    end
-    zombieMetatable = createZombie()
-end
-
-
-function manageZombies()
-    for i = 1, #zombiesTable do
-        local zombie = zombiesTable[i]
-        manageZombie(zombie)
-    end
-    processBoids()
-    navigationTimer.runTimerConst()
-end
-
-
-function manageZombie(zombie)
-    if zombie.ai.isActive then
-        if zombie:isAlive() then
-            zombieProcessAi(zombie)
-            diminishBodyAngVel(zombie.body, 0.8)
-        else
-            zombie.ai.isActive = false -- Disable dead zombie's ai.
-            zombieDie(zombie)
-        end
-    end
-end
-
-
---[[AI BEHAVIOR]]
-function zombieProcessAi(zombie)
-
-    -- Setting zombie target based on player vel.
-    if not zombieController.isActive then
-        zombie.ai.targetPos = zombie.getTargetPlayer()
-    end
-    zombie.ai.targetPos[2] = zombie.getPos()[2]
-
-    zombieProcessState(zombie)
-
-    -- Attack charge-up timer. 
-    if zombie.ai.state ~= zombie.ai.states.attacking then
-        zombie.timers.attack.chargeUp.time = zombie.timers.attack.chargeUp.deafult
-        zombie.sounds.chargeUpPlayed = false
-        -- DebugPrint('reset chargeup')
-    end
-
-    zombie.manageHealth()
-    zombie.runTimers()
-
-    if GetBool('savegame.mod.options.outline') then
-        zombie.drawOutline()
-    end
-
-end
-
-function zombieProcessState(zombie)
-
-    local distZombieToPlayer = CalcDist(zombie.getTr().pos, zombie.ai.targetPos)
-    if not zombie.isAlive() then -- zombie dead?
-        zombie.setState(zombie.ai.states.dead)
-
-    elseif distZombieToPlayer < zombie.ai.detection.distances.attacking then -- Close enough to attack.
-
-        zombie.setState(zombie.ai.states.attacking)
-        stateFunctions.attacking(zombie)
-
-    elseif distZombieToPlayer < zombie.ai.detection.distances.chasing then -- Close enough to chase.
-
-        zombie.setState(zombie.ai.states.chasing)
-        stateFunctions.chasing(zombie)
-
-    elseif distZombieToPlayer < zombie.ai.detection.distances.seeking then -- Close enough to seek.
-
-        zombie.setState(zombie.ai.states.seeking)
-        stateFunctions.seeking(zombie)
-
-    else -- Too far, so stay still.
-
-        zombie.setState(zombie.ai.states.still)
-        stateFunctions.still(zombie)
-    end
-
-end
-
-stateFunctions = {
-
-    still = function(zombie)
-        zombie.outlineColor = colors.black
-
-        local speed = 0
-        -- zombieChaseTarget(zombie, speed)
-        if isZombieOnGround(zombie) and zombie.isVelLow() then
-            zombieMoveWalk(zombie, 0, 1.5) -- hop in place
-            zombieKeepUpright(zombie)
-        end
-
-    end,
-
-    -- idle = function(zombie) end,
-    -- alert = function(zombie) end,
-
-    seeking = function(zombie)
-        zombie.outlineColor = colors.white
-
-        local speed = zombie.movement.speeds.random
-        zombieChaseTarget(zombie, speed)
-    end,
-
-
-    chasing = function(zombie)
-        zombie.outlineColor = colors.yellow
-
-        local speed = zombie.movement.speeds.run
-        zombieChaseTarget(zombie, speed)
-    end,
-
-
-    attacking = function(zombie)
-        zombie.outlineColor = colors.red
-
-        local speed = zombie.movement.speeds.attacking
-        zombieChaseTarget(zombie, speed)
-        zombieAttackPlayer(zombie)
-    end,
-
-}
-
-
---[[ZOMBIE MOVEMENT]]
-function isZombieOnGround(zombie)
-
-    local zTr = zombie.getTr()
-
-    local rcTr = Transform(VecAdd(zTr.pos, Vec(0,0.5,0)), QuatLookDown(zTr.pos))
-    local hit, hitPos, hitShape = raycastFromTransform(rcTr, 0.5, 0.5, zombie.body)
-
-    local isRcBodyZombie = HasTag(GetShapeBody(hitShape), "ai_zombie")
-    if hit and not isRcBodyZombie or IsPointInWater(zombie.getTr().pos) then
-        return true
-    end
-    return false
-end
-
-
-function zombieKeepUpright(zombie, rotRate)
-    local zTr = zombie.getTr()
-    zTr.rot[1] = zTr.rot[1] * 0.9999
-    zTr.rot[3] = zTr.rot[3] * 0.9999
-    zombie.setTr(zTr)
-end
-
-
-function zombieLookAt(zombie, targetPos, rate)
-    local zTr = zombie.getTr()
-    local zTrNew = TransformCopy(zTr)
-
-    local lookRot = QuatLookAt(zTr.pos, targetPos)
-    local zTrRot = QuatSlerp(zTr.rot, lookRot, rate or 0.4)  -- Look left and right only.
-    zTr.rot[1] = 0
-    zTr.rot[3] = 0
-    zTrNew.rot = zTrRot
-
-    zombie.setTr(zTrNew)
-end
-
-
-function zombieMoveWalk(zombie, speed, hopAmt, sideAmt, velDir)
-    if velDir == nil then
-        local zTr = zombie.getTr()
-        local zVel = GetBodyVelocity(zombie.body)
-        local zFwdPos = TransformToParentPoint(zTr, Vec(sideAmt or 0, -hopAmt or -1, speed or 3))
-        local zPos = zTr.pos
-        local velSub = VecSub(zPos, zFwdPos)
-        SetBodyVelocity(zombie.body, velSub)
-    else
-        SetBodyVelocity(zombie.body, velDir)
-    end
-end
-
-
-function zombieMoveJump(zombie, jumpForce)
-    if jumpForce == nil then
-        jumpForce = 5
-    end
-    local zTr = zombie.getTr()
-    local jumpVel = TransformToParentPoint(zTr, Vec(0, jumpForce, -jumpForce * 0.8))
-    local jumpDir = VecSub(jumpVel, zTr.pos)
-    SetBodyVelocity(zombie.body, jumpDir)
-end
-
-
-function zombieAttackPlayer(zombie)
-
-    -- Charge up hit.
-    if zombie.timers.attack.chargeUp.timer <= 0 then -- charge up timer.
-
-        -- DebugPrint('Charging'..sfnTime())
-
-        -- Hit player
-        if zombie.timers.attack.hit.timer <= 0 then -- attack timer.
-            zombie.timers.attack.hit.timer = 60/zombie.timers.attack.hit.rpm
-
-            local playerPos = game.ppos
-            -- zombieLookAt(zombie, playerPos, 0.1)
-
-            -- Hit values
-            local zTr = zombie.getTr()
-            local zFwdPos = Vec(0,1,-2)
-            local attackPos = TransformToParentPoint(zTr, zFwdPos)
-            local zombieToPlayerDist = CalcDist(attackPos, playerPos)
-            DebugLine(attackPos, playerPos)
-
-            -- Hit player
-            if zombieToPlayerDist < zombie.ai.attacking.distance then
-                SetPlayerHealth(GetPlayerHealth() - zombie.ai.attacking.damage) -- Decrease player health.
-                -- DebugPrint('hit'..sfnTime())
-                sounds.play.hit(zombie)
-            end
-
-        else
-            -- countdown until next hit.
-            zombie.timers.attack.hit.timer = zombie.timers.attack.hit.timer - GetTimeStep() 
-        end
-
-    else
-        -- countdown until next chargeup.
-        zombie.timers.attack.chargeUp.timer = zombie.timers.attack.chargeUp.timer - GetTimeStep()
-
-    end
-
-    -- Play sounds once per chargeup.
-    if zombie.sounds.chargeUpPlayed == false then
-        zombie.sounds.chargeUpPlayed = true
-        sounds.play.growl(zombie)
-    end
-
-end
-
-function zombieChaseTarget(zombie, speed)
-
-    if zombie.isVelLow() then
-
-        -- Keep zombie stable
-        zombieLookAt(zombie, zombie.ai.targetPos, 0.3)
-        zombieKeepUpright(zombie)
-
-        if isZombieOnGround(zombie) then
-            local zVel = GetBodyVelocity(zombie.body)
-
-            zombie.movement.speed = speed
-            zombie.raycastNavigate()
-
-            -- if boidsData.timer.time <= 0 then -- Timed for performance.
-            --     boidsData.timer.time = 60/boidsData.timer.rpm
-                zombie.boidsNavigate()
-            -- end
-
-            local zVelRaycast = GetBodyVelocity(zombie.body)
-            local zVelLerp = VecLerp(zVel, zVelRaycast, 0.5)
-            SetBodyVelocity(zombie.body, zVelLerp)
-        end
-
-    end
-
-end
-
-
--- [[ZOMBIE MISC]]
+#version 2
 function zombieDie(zombie)
     zombie.ai.isActive = false -- Disable dead zombie's ai.
     if zombie:isAlive() == false then
@@ -297,6 +7,3 @@
     end
 end
 
--- Times when to process zombie navigation for better performance.
-navigationTimer = { time = 0, rpm = 5000,}
-navigationTimer.runTimerConst = function() navigationTimer.time = navigationTimer.time - GetTimeStep() end
```

---

# Migration Report: zombieMod\scripts\zombieConstructor.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/zombieMod\scripts\zombieConstructor.lua
+++ patched/zombieMod\scripts\zombieConstructor.lua
@@ -1,13 +1,4 @@
--- ====================================================================================================
--- Basic Ai Zombies - by: Cheejins
--- ====================================================================================================
-
--- ----------------------------------------------------------------------------------------------------
--- This script handles the creation of a zombie instance.
--- ----------------------------------------------------------------------------------------------------
-
-
---[[ZOMBIE CONSTRUCTION]]
+#version 2
 function createZombie(body, id) -- Create zombie.
 
     local zombie = {}
@@ -47,7 +38,6 @@
         end
     end
 
-
     --[[AI]]
     zombie.health = 100
     zombie.ai = {
@@ -95,12 +85,10 @@
         },
     }
 
-
     local randomSpeed = rdm(3,5)
     if randomSpeed < 2 then
         randomSpeed = 2
     end
-
 
     --[[Physics]]
     zombie.movement = {
@@ -134,7 +122,6 @@
         deathVal = nil,
     }
     zombie.mass.deathVal = zombie.mass.start * zombie.mass.deathPercentage
-
 
     --[[Misc]]
     zombie.outlineColor = colors.white
@@ -225,13 +212,13 @@
 
         local zTr = zombie.getTr()
 
-        local playerPos = GetPlayerTransform().pos
+        local playerPos = GetPlayerTransform(playerId).pos
         local distZombieToPlayerPos = CalcDist(zTr.pos, playerPos)
         local distZombieToPlayerPosScaled = distZombieToPlayerPos/20
 
         if distZombieToPlayerPosScaled > 10 and distZombieToPlayerPos < 30 then
             distZombieToPlayerPosScaled = 10
-            local playerVel = GetPlayerVelocity()
+            local playerVel = GetPlayerVelocity(playerId)
             local playerVelScaled = VecScale(playerVel, distZombieToPlayerPosScaled)
             return VecAdd(playerPos, playerVelScaled)
         end
@@ -248,10 +235,9 @@
 
     zombie.drawOutline = function()
         local c = VecCopy(zombie.outlineColor)
-        local a = 4/CalcDist(zombie.getPos(), GetPlayerTransform().pos)
+        local a = 4/CalcDist(zombie.getPos(), GetPlayerTransform(playerId).pos)
         DrawBodyOutline(zombie.body, c[1], c[2], c[3], a)
     end
-
 
     zombie.raycastNavigate = function ()
 
@@ -287,7 +273,6 @@
             -- DebugLine(hitPosLower, TransformToParentPoint(rc.lower.tr, Vec(0,0,-rc.lower.dist)), 0, 1, 0)
         end
 
-
         local hitUpper, hitPosUpper, hitShapeUpper = nil,nil,nil
         if hitLower then
             -- upper
@@ -343,7 +328,6 @@
         end
 
     end
-
 
     zombie.boidsNavigate = function ()
 
@@ -394,6 +378,6 @@
 
     end
 
-
     return zombie
 end
+

```

---

# Migration Report: zombieMod\scripts\zombieController.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/zombieMod\scripts\zombieController.lua
+++ patched/zombieMod\scripts\zombieController.lua
@@ -1,22 +1,10 @@
-#include "scripts/utility.lua"
-#include "scripts/zombie.lua"
-
--- ====================================================================================================
--- Basic Ai Zombies - by: Cheejins
--- ====================================================================================================
-
--- ----------------------------------------------------------------------------------------------------
--- This script handles the creation of a zombie instance.
--- ----------------------------------------------------------------------------------------------------
-
-
+#version 2
 function initZombieController()
     zombieController = {active = false, pos = Vec(0,0,0),}
 
     RegisterTool('zombieController','Zombie Controller', 'MOD/zombieMod/vox/zombieController.vox')
-    SetBool('game.tool.zombieController.enabled', true)
+    SetBool('game.tool.zombieController.enabled', true, true)
 end
-
 
 function runZombieController()
 
@@ -70,4 +58,5 @@
         PointLight(VecAdd(zombieController.pos, Vec(0,1,0)), 0, 1, 0, 3)
         DebugLine((zombieController.pos), VecAdd(zombieController.pos, Vec(0,10,0)), 0.5, 1, 0.5)
     end
-end+end
+

```

---

# Migration Report: zombieMod\scripts\zombieRadar.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/zombieMod\scripts\zombieRadar.lua
+++ patched/zombieMod\scripts\zombieRadar.lua
@@ -1,8 +1,4 @@
--- ====================================================================================================
--- Basic Ai Zombies - by: Cheejins
--- ====================================================================================================
-
-
+#version 2
 local zr = {
     static = {
         bounds = {       
@@ -23,14 +19,12 @@
     },
 }
 
-
 function runZombieRadar()
     if GetString('savegame.mod.zombieRadar.corner') ~= 'off' then
         positionRadar()
         drawRadar()
     end
 end
-
 
 function positionRadar()
 
@@ -56,7 +50,6 @@
     UiTranslate(translate[1], translate[2])
 end
 
-
 function drawRadar()
     UiPush()
 
@@ -75,7 +68,7 @@
             UiImageBox('MOD/zombieMod/img/radar/triangle.png', zr.static.blips.player.width, zr.static.blips.player.height)
 
             -- Zombie blips
-            local pTr = GetPlayerTransform()
+            local pTr = GetPlayerTransform(playerId)
             for i = 1, #zombiesTable do
 
                 local z = zombiesTable[i]
@@ -103,3 +96,4 @@
 
     UiPop()
 end
+

```
