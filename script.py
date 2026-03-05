import docker
import os


def run_in_euclid_container(image_path, out_psf="euclid_model.psf"):
    client = docker.from_env()

    # Get absolute path for Docker volume mounting
    abs_path = os.path.abspath(os.path.dirname(image_path))
    file_name = os.path.basename(image_path)
    cat_name = "prelim_cat.ldac"

    # Define the volume mapping: {host_path: {'bind': container_path, 'mode': 'rw'}}
    print(f"Mounting host directory: {abs_path} to container at /data")
    volumes = {abs_path: {"bind": "/data", "mode": "rw"}}

    print(f"--- Launching Container with mount: {abs_path} ---")

    try:
        # 1. Run Source-Extractor
        # We use 'source-extractor' as it is the standard name in Debian/Ubuntu
        sex_cmd = (
            "source-extractor "
            f"{file_name} "
            "-c /data/default.sex "  # Explicitly point to config
            "-PARAMETERS_NAME /data/default.param "  # Explicitly point to params
            "-FILTER_NAME /data/default.conv "  # Explicitly point to filter
            "-CATALOG_NAME /data/prelim_cat.fits "
            "-CATALOG_TYPE FITS_LDAC "
            # "-PSF_NAME /data/none"
        )
        print("Running Source-Extractor...")
        client.containers.run(
            "euclid-psf-env",
            sex_cmd,
            volumes=volumes,
            working_dir="/data",
            remove=False,
        )

        # 2. Run PSFEx
        # psf_cmd = f"psfex {cat_name} -PSF_NAMETAG {out_psf.replace('.psf', '')}"
        psf_cmd = (
            "psfex "
            "/data/prelim_cat.fits "
            "-c /data/default.psfex "  # Explicitly point to psfex config
            f"-PSF_NAMETAG {out_psf.replace('.psf', '')}"
        )
        print("Running PSFEx...")
        client.containers.run(
            "euclid-psf-env", psf_cmd, volumes=volumes, working_dir="/data", remove=True
        )

        print(f"✅ Success! Your PSF model should be in: {abs_path}/{out_psf}")

    except docker.errors.ContainerError as e:
        print(f"❌ Container Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example:
run_in_euclid_container(
    "EUC_MER_BGSUB-MOSAIC-VIS_TILE101158277-BB647A_20240122T115602.395130Z_00.00.fits"
)
