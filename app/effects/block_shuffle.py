"""Block shuffle effect."""
import numpy as np
import random
from typing import Dict, Any, Optional
from app.effects.base import Effect


class BlockShuffle(Effect):
    """Shuffle image blocks with optional rotation/flip."""
    
    name = "Block Shuffle"
    description = "Перемешивает мозаику блоков, сохраняя узнаваемость."
    
    @classmethod
    def default_params(cls) -> Dict[str, Any]:
        return {
            "block_size": 32,
            "shuffle_strength": 0.3,
            "block_transform": "none",  # none, rotate, flip, jitter
            "seed": 42
        }
    
    @classmethod
    def apply(cls, image: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        block_size = int(params.get("block_size", 32))
        shuffle_strength = params.get("shuffle_strength", 0.3)
        block_transform = params.get("block_transform", "none")
        seed = params.get("seed", 42)
        
        h, w = image.shape[:2]
        result = image.copy()
        
        # Calculate number of blocks
        num_blocks_y = (h + block_size - 1) // block_size
        num_blocks_x = (w + block_size - 1) // block_size
        total_blocks = num_blocks_y * num_blocks_x
        
        random.seed(seed)
        
        # Generate shuffle order
        num_shuffled = int(total_blocks * shuffle_strength)
        shuffled_indices = random.sample(range(total_blocks), num_shuffled)
        shuffle_map = list(range(total_blocks))
        random.shuffle(shuffled_indices)
        
        # Create mapping
        for i, orig_idx in enumerate(shuffled_indices):
            shuffle_map[orig_idx] = shuffled_indices[(i + 1) % len(shuffled_indices)]
        
        # Extract and transform blocks
        blocks = []
        for by in range(num_blocks_y):
            for bx in range(num_blocks_x):
                y1 = by * block_size
                y2 = min(y1 + block_size, h)
                x1 = bx * block_size
                x2 = min(x1 + block_size, w)
                
                block = image[y1:y2, x1:x2].copy()
                
                # Apply block transform
                block = cls._transform_block(block, block_transform, seed + by * num_blocks_x + bx)
                blocks.append(block)
        
        # Reassemble blocks in shuffled order
        for by in range(num_blocks_y):
            for bx in range(num_blocks_x):
                block_idx = by * num_blocks_x + bx
                target_idx = shuffle_map[block_idx]
                
                # Only shuffle if this block is in shuffled set
                if block_idx in shuffled_indices:
                    source_by = target_idx // num_blocks_x
                    source_bx = target_idx % num_blocks_x
                else:
                    source_by = by
                    source_bx = bx
                
                y1 = by * block_size
                y2 = min(y1 + block_size, h)
                x1 = bx * block_size
                x2 = min(x1 + block_size, w)
                
                source_y1 = source_by * block_size
                source_y2 = min(source_y1 + block_size, h)
                source_x1 = source_bx * block_size
                source_x2 = min(source_x1 + block_size, w)
                
                src_h = source_y2 - source_y1
                src_w = source_x2 - source_x1
                dst_h = y2 - y1
                dst_w = x2 - x1
                
                if src_h == dst_h and src_w == dst_w:
                    result[y1:y2, x1:x2] = blocks[target_idx]
        
        return result
    
    @classmethod
    def _transform_block(cls, block: np.ndarray, transform: str, seed: int) -> np.ndarray:
        """Apply transformation to a single block."""
        if transform == "none":
            return block
        
        random.seed(seed)
        result = block.copy()
        
        if transform == "rotate":
            k = random.randint(1, 3)  # 90, 180, or 270 degrees
            result = np.rot90(result, k)
        elif transform == "flip":
            if random.random() < 0.5:
                result = np.flip(result, axis=0)  # Vertical flip
            else:
                result = np.flip(result, axis=1)  # Horizontal flip
        elif transform == "jitter":
            # Slight random offset (clamp to block size)
            offset_y = random.randint(-2, 2)
            offset_x = random.randint(-2, 2)
            if offset_x != 0 or offset_y != 0:
                h, w = block.shape[:2]
                result = np.roll(result, (offset_y, offset_x), axis=(0, 1))
        
        return result
    
    @classmethod
    def randomize(cls, params: Dict[str, Any], seed: Optional[int] = None) -> Dict[str, Any]:
        import random
        if seed is not None:
            random.seed(seed)
        
        params = params.copy()
        params["block_size"] = random.choice([8, 16, 32, 64, 128])
        params["shuffle_strength"] = random.uniform(0.1, 0.5)
        params["block_transform"] = random.choice(["none", "rotate", "flip", "jitter"])
        params["seed"] = random.randint(0, 2**31 - 1)
        return params
    
    @classmethod
    def get_intensity_param(cls) -> Optional[str]:
        return "shuffle_strength"

