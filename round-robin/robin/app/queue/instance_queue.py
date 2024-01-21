from .instance import Instance


class InstanceQueue:
    instance_list = []

    def __init__(self) -> None:
        pass

    def add(self, instance: Instance):
        """Add new instance to the round

        Args:
            instance (Instance): Where to forward the post to
        """
        self.instance_list.append(instance)

    def pop(self, payload):
        """Remove an instance out of queue and
        put it back in the queue
        """
        response = None
        while len(self.instance_list) != 0:
            latest_instance = self.instance_list.pop(0)
            response = latest_instance.forward(payload)

            if response != None:
                # Put it back to the queue
                self.instance_list.append(latest_instance)
                return response

        # Exhausted all the instances in the queue list
        raise Exception("No instances left to pass request to")
