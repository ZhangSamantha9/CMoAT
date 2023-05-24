import os
import sys
package_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(package_dir)
# sys.path.append(package_dir)
sys.path.append(parent_dir)