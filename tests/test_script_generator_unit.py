"""
Unit tests for script_generator.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from script_generator import clean_script, extract_emotional_markers


def test_clean_script():
    """Test that emotional markers are removed from script."""
    script = "What happens if [pause] you stop drinking water? [intense] It's dangerous!"
    cleaned = clean_script(script)
    
    assert "[pause]" not in cleaned
    assert "[intense]" not in cleaned
    assert "What happens if" in cleaned
    assert "you stop drinking water?" in cleaned


def test_clean_script_multiple_markers():
    """Test cleaning script with multiple markers."""
    script = "[slow] Kya hoga [pause] agar aap paani peena band kar do? [intense] Bahut khatarnak!"
    cleaned = clean_script(script)
    
    assert "[slow]" not in cleaned
    assert "[pause]" not in cleaned
    assert "[intense]" not in cleaned
    assert "Kya hoga" in cleaned


def test_extract_emotional_markers():
    """Test extraction of emotional markers from script."""
    script = "What happens if [pause] you stop drinking water? [intense] It's dangerous!"
    markers = extract_emotional_markers(script)
    
    assert len(markers) == 2
    assert markers[0]['marker'] == 'pause'
    assert markers[1]['marker'] == 'intense'


def test_extract_emotional_markers_empty():
    """Test extraction when no markers present."""
    script = "What happens if you stop drinking water? It's dangerous!"
    markers = extract_emotional_markers(script)
    
    assert len(markers) == 0


def test_extract_emotional_markers_all_types():
    """Test extraction of all marker types."""
    script = "[slow] Start [pause] middle [intense] end [excited] more [calm] finish"
    markers = extract_emotional_markers(script)
    
    assert len(markers) == 5
    marker_types = [m['marker'] for m in markers]
    assert 'slow' in marker_types
    assert 'pause' in marker_types
    assert 'intense' in marker_types
    assert 'excited' in marker_types
    assert 'calm' in marker_types


def test_clean_script_preserves_content():
    """Test that cleaning preserves the actual content."""
    script = "[slow] Kya hoga agar [pause] aap 3 din tak paani nahi piyenge? [intense] Shocking results!"
    cleaned = clean_script(script)
    
    # Check that content is preserved
    assert "Kya hoga agar" in cleaned
    assert "aap 3 din tak paani nahi piyenge?" in cleaned
    assert "Shocking results!" in cleaned
    
    # Check that markers are removed
    assert "[" not in cleaned
    assert "]" not in cleaned


if __name__ == "__main__":
    print("Running unit tests for script_generator.py\n")
    print("=" * 60)
    
    tests = [
        ("test_clean_script", test_clean_script),
        ("test_clean_script_multiple_markers", test_clean_script_multiple_markers),
        ("test_extract_emotional_markers", test_extract_emotional_markers),
        ("test_extract_emotional_markers_empty", test_extract_emotional_markers_empty),
        ("test_extract_emotional_markers_all_types", test_extract_emotional_markers_all_types),
        ("test_clean_script_preserves_content", test_clean_script_preserves_content),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            print(f"✅ {test_name} - PASSED")
            passed += 1
        except AssertionError as e:
            print(f"❌ {test_name} - FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"\nResults: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✅ All tests passed!")
    else:
        print(f"❌ {failed} test(s) failed")

