export LD_LIBRARY_PATH="./inference_engine_vpu_arm/opencv/lib:/opt/intel/opencl:./inference_engine_vpu_arm/deployment_tools/inference_engine/external/hddl/lib:./inference_engine_vpu_arm/deployment_tools/inference_engine/external/gna/lib:./inference_engine_vpu_arm/deployment_tools/inference_engine/external/mkltiny_lnx/lib:./inference_engine_vpu_arm/deployment_tools/inference_engine/external/omp/lib:./inference_engine_vpu_arm/deployment_tools/inference_engine/lib/raspbian_9/armv7l"
export PYTHONPATH="./inference_engine_vpu_arm/python/python3.5:./inference_engine_vpu_arm/python/python3.5/armv7l:./inference_engine_vpu_arm/deployment_tools/model_optimizer"

python3 utils/skill.py
