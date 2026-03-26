import asyncio
from aiortc.contrib.signaling import TcpSocketSignaling
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCIceCandidate

async def _webrtc_init(ip_address: str = "0.0.0.0", port: int = 8080):

    signaling = TcpSocketSignaling(ip_address, port)
    pc = RTCPeerConnection()

    try:
        await signaling.connect()

        connected_event = asyncio.Event()

        @pc.on("connectionstatechange")
        def on_statechange():
            print(pc.connectionState)
            if pc.connectionState in ("connected", "completed"):
                connected_event.set()

        @pc.on("icecandidate")
        def on_icecandidate(candidate):
            if candidate is not None:
                asyncio.create_task(signaling.send(candidate))

        dc = pc.createDataChannel("data")
        channel_open = asyncio.Event()

        @dc.on("open")
        def on_open():
            print("DataChannel open")
            channel_open.set()

        @dc.on("message")
        def on_message(message):
            print("Desktop got:", message)

        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)
        await signaling.send(pc.localDescription)

        async def receive_signaling():
            while True:
                obj = await signaling.receive()
                if isinstance(obj, RTCSessionDescription):
                    await pc.setRemoteDescription(obj)
                    print("Desktop: remote description set")
                elif isinstance(obj, RTCIceCandidate):
                    await pc.addIceCandidate(obj)
                elif obj is None:
                    print("Desktop: signaling ended")
                    break

        signaling_task = asyncio.create_task(receive_signaling())

        await connected_event.wait()
        signaling_task.cancel()

        print("Desktop: connected, waiting for channel to open")
        await asyncio.wait_for(channel_open.wait(), timeout=10)

        try:
            print(f"About to send, channel ready: {dc.readyState}")
            dc.send("Hi from PC")
            print("Message sent successfully")
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Failed to send: {e}")

        while pc.connectionState in ("connected", "completed"):
            await asyncio.sleep(1)

    finally:
        print("Reached close.")
        await pc.close()