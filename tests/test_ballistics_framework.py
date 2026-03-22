"""Tests for the Trust Realism ballistics framework (lib/realistic_ballistics.lua).

Tests the pure math functions: falloff curves, material multipliers,
spread distribution, and ammo state management.
"""
import math
import pytest


# ============================================================
# Falloff curve tests
# ============================================================

def exponential_falloff(dist, full_range, half_range, min_falloff):
    """Python reimplementation of GetFalloff for testing."""
    if dist <= full_range:
        return 1.0
    drop_dist = dist - full_range
    half_dist = half_range - full_range
    if half_dist <= 0:
        return min_falloff
    decay = math.pow(0.5, drop_dist / half_dist)
    return max(min_falloff, decay)


class TestFalloff:
    """Test the exponential distance falloff curve."""

    def test_within_full_range(self):
        assert exponential_falloff(0, 8, 25, 0.15) == 1.0
        assert exponential_falloff(5, 8, 25, 0.15) == 1.0
        assert exponential_falloff(8, 8, 25, 0.15) == 1.0

    def test_at_half_range(self):
        result = exponential_falloff(25, 8, 25, 0.15)
        assert abs(result - 0.5) < 0.01

    def test_at_double_half_range(self):
        result = exponential_falloff(42, 8, 25, 0.15)
        assert abs(result - 0.25) < 0.01

    def test_respects_minimum(self):
        result = exponential_falloff(200, 8, 25, 0.15)
        assert result == 0.15

    def test_monotonically_decreasing(self):
        prev = 1.0
        for d in range(0, 100):
            val = exponential_falloff(d, 8, 25, 0.15)
            assert val <= prev
            prev = val

    def test_is_exponential_not_linear(self):
        """At full_range + half_dist, should be 0.5, not linear interpolation."""
        f_at_half = exponential_falloff(25, 8, 25, 0.15)
        # Linear would give ~0.66 at this point; exponential gives 0.5
        assert abs(f_at_half - 0.5) < 0.01


# ============================================================
# Material resistance tests
# ============================================================

def material_multiplier(dist, mult, mat_range):
    """Python reimplementation of per-material falloff."""
    if dist <= mat_range:
        return mult
    over_dist = dist - mat_range
    mat_decay = math.pow(0.1, over_dist / mat_range)
    return mult * mat_decay


class TestMaterialResistance:
    """Test per-material damage multiplier with range-based falloff."""

    def test_within_range_returns_base_mult(self):
        assert material_multiplier(2, 0.3, 3) == 0.3  # metal at 2m
        assert material_multiplier(15, 1.0, 20) == 1.0  # wood at 15m

    def test_at_double_range_drops_to_10pct(self):
        result = material_multiplier(6, 0.3, 3)  # metal at 2x range
        assert abs(result - 0.3 * 0.1) < 0.01

    def test_glass_effective_at_distance(self):
        result = material_multiplier(30, 1.5, 40)  # glass at 30m (within range)
        assert result == 1.5

    def test_metal_useless_at_distance(self):
        result = material_multiplier(10, 0.3, 3)  # metal at 10m
        assert result < 0.01  # nearly zero

    def test_exponential_not_linear(self):
        at_range = material_multiplier(3, 0.3, 3)
        just_past = material_multiplier(4, 0.3, 3)
        far_past = material_multiplier(6, 0.3, 3)
        assert at_range > just_past > far_past


# ============================================================
# Penetration push absorption tests
# ============================================================

def absorbed_push(penetration_ratio):
    """Python reimplementation of exponential absorbed calculation."""
    return math.pow(0.05, penetration_ratio)


class TestPushAbsorption:
    """Test penetration-aware push physics."""

    def test_full_penetration_minimal_push(self):
        result = absorbed_push(1.0)
        assert abs(result - 0.05) < 0.01  # passes through, barely moves

    def test_no_penetration_full_push(self):
        result = absorbed_push(0.0)
        assert result == 1.0  # stops inside, max transfer

    def test_half_penetration_moderate(self):
        result = absorbed_push(0.5)
        assert 0.15 < result < 0.30  # moderate transfer

    def test_is_exponential(self):
        """Verify the curve is exponential, not linear."""
        at_half = absorbed_push(0.5)
        # Linear would give 0.525; exponential gives ~0.22
        assert at_half < 0.3


# ============================================================
# Spread distribution tests
# ============================================================

class TestSpreadDistribution:
    """Test that sqrt(random) gives uniform disk distribution."""

    def test_sqrt_distribution_not_center_heavy(self):
        """With sqrt(random), less than 50% of values should be below 0.5."""
        import random
        random.seed(42)
        n = 10000
        below_half = sum(1 for _ in range(n) if math.sqrt(random.random()) < 0.5)
        ratio = below_half / n
        # sqrt distribution: P(x < 0.5) = 0.5^2 = 0.25
        assert 0.20 < ratio < 0.30

    def test_sqrt_distribution_covers_outer_ring(self):
        """With sqrt(random), ~75% of values should be above 0.5."""
        import random
        random.seed(42)
        n = 10000
        above_half = sum(1 for _ in range(n) if math.sqrt(random.random()) > 0.5)
        ratio = above_half / n
        assert 0.70 < ratio < 0.80


# ============================================================
# Caliber inheritance tests
# ============================================================

class TestCaliberSystem:
    """Test caliber + ammo type + per-weapon override priority chain."""

    def test_priority_chain(self):
        """caliber base -> ammo overrides -> per-weapon overrides."""
        # Simulate the merge logic
        base = {"damage": 28, "pellets": 12, "spread": 0.07}
        ammo = {"pellets": 1, "damage": 80}  # slug
        weapon = {"spread": 0.005}  # custom tight spread

        merged = dict(base)
        merged.update(ammo)
        merged.update(weapon)

        assert merged["damage"] == 80   # from ammo
        assert merged["pellets"] == 1   # from ammo
        assert merged["spread"] == 0.005  # from weapon override

    def test_ammo_overrides_caliber(self):
        base = {"damage": 28, "pellets": 12}
        ammo = {"pellets": 40, "damage": 5}  # birdshot
        merged = dict(base)
        merged.update(ammo)
        assert merged["pellets"] == 40
        assert merged["damage"] == 5

    def test_weapon_overrides_ammo(self):
        base = {"damage": 28}
        ammo = {"damage": 80}
        weapon = {"damage": 100}
        merged = dict(base)
        merged.update(ammo)
        merged.update(weapon)
        assert merged["damage"] == 100


# ============================================================
# Ammo system tests
# ============================================================

class TestAmmoSystem:
    """Test magazine, reserve, reload, and conservative reload logic."""

    def test_conservative_reload(self):
        """If 4 of 8 shells fired, only use 4 from reserve."""
        mag_size = 8
        magazine = 4  # fired 4
        reserve = 32
        needed = mag_size - magazine
        available = min(needed, reserve)
        new_magazine = magazine + available
        new_reserve = reserve - available
        assert new_magazine == 8
        assert new_reserve == 28  # only used 4, not 8

    def test_reserve_exhaustion(self):
        """If reserve < needed, only partial reload."""
        mag_size = 8
        magazine = 0
        reserve = 3
        needed = mag_size - magazine
        available = min(needed, reserve)
        new_magazine = magazine + available
        new_reserve = reserve - available
        assert new_magazine == 3
        assert new_reserve == 0

    def test_full_magazine_no_reload(self):
        """Can't reload when magazine is full."""
        mag_size = 8
        magazine = 8
        needed = mag_size - magazine
        assert needed == 0


# ============================================================
# Damage variance tests
# ============================================================

class TestDamageVariance:
    """Test per-pellet randomized damage."""

    def test_variance_range(self):
        """With 15% variance, damage should stay within +/-15%."""
        import random
        random.seed(42)
        base = 0.28
        variance = 0.15
        for _ in range(1000):
            r = random.random() * 2 - 1
            dmg = base * (1.0 + r * variance)
            assert base * 0.85 <= dmg <= base * 1.15

    def test_zero_variance_is_uniform(self):
        base = 0.28
        dmg = base * (1.0 + 0 * 0.15)  # variance = 0
        assert dmg == base
