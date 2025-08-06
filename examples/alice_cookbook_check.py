#!/usr/bin/env python3
"""
Example: Check if Alice's cookbook recipes appear in training data.

This example demonstrates how to use AEGIS Bloom to check if content
might have been included in a model's training dataset.
"""

import tempfile
from pathlib import Path
from aegis import BloomFilter

def main():
    """Run the Alice cookbook copyright check example."""
    
    # Create some sample training data
    training_data = [
        "The secret to perfect chocolate chip cookies is using brown butter.",
        "For fluffy pancakes, don't overmix the batter - lumps are okay!",
        "When making bread, let the dough rise slowly in a cool place.",
        "The best pasta sauce starts with slowly caramelized onions.",
        "For crispy roasted vegetables, use high heat and don't overcrowd.",
    ]
    
    # Alice's cookbook content (some overlaps with training data)
    alice_recipes = [
        "The secret to perfect chocolate chip cookies is using brown butter and sea salt.",
        "My grandmother's apple pie recipe uses tart Granny Smith apples.",
        "For the best scrambled eggs, cook them low and slow with butter.",
    ]
    
    print("🛡️ AEGIS Bloom Copyright Check Example")
    print("=" * 50)
    
    # Create temporary directory for training data
    with tempfile.TemporaryDirectory() as temp_dir:
        training_dir = Path(temp_dir) / "training_data"
        training_dir.mkdir()
        
        # Write training data files
        for i, recipe in enumerate(training_data):
            recipe_file = training_dir / f"recipe_{i+1}.txt"
            recipe_file.write_text(recipe)
        
        print(f"📁 Created {len(training_data)} training files")
        
        # Build bloom filter from training data
        print("🔨 Building bloom filter...")
        bloom = BloomFilter.from_directory(
            training_dir,
            chunk_size=64,  # Smaller chunks for this example
            false_positive_rate=0.01  # 1% false positive rate
        )
        
        print(f"✅ Bloom filter built with {bloom.metadata['items_added']} chunks")
        
        # Check Alice's recipes
        print("\n📖 Checking Alice's cookbook recipes:")
        print("-" * 40)
        
        for i, recipe in enumerate(alice_recipes, 1):
            result = bloom.check(recipe)
            
            # Create status emoji and message
            if result == "MAYBE_PRESENT":
                status = "⚠️ MAYBE_PRESENT"
                message = "Potential copyright concern - manual review needed"
            else:
                status = "✅ NOT_PRESENT" 
                message = "Safe to use - not in training data"
            
            print(f"Recipe {i}: {status}")
            print(f"   Text: \"{recipe[:50]}...\"")
            print(f"   Status: {message}")
            print()
        
        # Example of saving/loading bloom filters
        bloom_file = Path(temp_dir) / "cookbook_training.bloom"
        bloom.save(bloom_file)
        
        print(f"💾 Saved bloom filter to {bloom_file.name}")
        print(f"   File size: {bloom_file.stat().st_size:,} bytes")
        
        # Load and test
        loaded_bloom = BloomFilter.load(bloom_file)
        test_result = loaded_bloom.check(alice_recipes[0])
        print(f"🔄 Loaded bloom filter test: {test_result}")

if __name__ == "__main__":
    main()
