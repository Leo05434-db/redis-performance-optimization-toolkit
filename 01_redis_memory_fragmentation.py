# ========================================================================
# REDIS TOOLKIT: MEMORY FRAGMENTATION & SWAP AUDITOR
# Requires: pip install redis
# ========================================================================
import redis

def audit_redis_memory(host='localhost', port=6379, db=0, password=None):
    try:
        # Establish a secure connection with a strict timeout
        r = redis.Redis(host=host, port=port, db=db, password=password, socket_timeout=2, decode_responses=True)
        info = r.info('memory')
        
        used_memory = info['used_memory_human']
        rss_memory = info['used_memory_rss_human']
        frag_ratio = info['mem_fragmentation_ratio']
        
        print("=== Redis Memory Diagnostics ===")
        print(f"Actual Data Size in Cache: {used_memory}")
        print(f"Total Operating System RAM Allocated (RSS): {rss_memory}")
        print(f"Memory Fragmentation Ratio: {frag_ratio}")
        print("---------------------------------")
        
        # Interpret the metrics for the buyer
        if frag_ratio > 1.5:
            print("ALERT: High Memory Fragmentation! Redis is wasting system RAM.")
            print("Solution: Enable active defragmentation in your redis.conf file:")
            print("          CONFIG SET activedefrag yes")
        elif frag_ratio < 1.0:
            print("CRITICAL CRASH RISK: Operating system is swapping Redis memory to disk!")
            print("Solution: Your server is out of physical RAM. Squeeze cache size or upgrade host instance.")
        else:
            print("HEALTHY: Redis memory allocations are structured cleanly inside RAM.")
            
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    # Example local connection check
    audit_redis_memory()
