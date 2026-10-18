import docker

client = docker.from_env()

print("Building image...")
client.images.build(path=".", tag="flask-apparmor")

print("Running container with AppArmor profile...")

container = client.containers.run(
    "flask-apparmor",
    name="flask-sdk-test",
    ports={"5000/tcp": 5000},
    security_opt=["apparmor=flask-apparmor-profile"],
    detach=True
)

print(f"Container started: {container.short_id}")

container_info = client.api.inspect_container(container.id)
print("AppArmor profile:", container_info["AppArmorProfile"])

container.stop()
container.remove()

print("Container stopped and removed.")
