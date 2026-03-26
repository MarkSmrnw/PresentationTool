import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCIceCandidate
from aiortc.contrib.signaling import TcpSocketSignaling

async def run(pc: RTCPeerConnection, signaling: TcpSocketSignaling):

    await signaling.connect()

    connected_event = asyncio.Event()

    @pc.on("connectionstatechange")
    def on_statechange():
        print("Phone state:", pc.connectionState)
        if pc.connectionState in ("connected", "completed"):
            connected_event.set()

    @pc.on("icecandidate")
    def on_icecandidate(candidate):
        if candidate is not None:
            asyncio.create_task(signaling.send(candidate))

    channel_open = asyncio.Event()

    @pc.on("datachannel")
    def on_channel(channel):
        print("Phone got datachannel:", channel.label)

        @channel.on("open")
        def on_open():
            print("Phone channel open")
            channel_open.set()

        @channel.on("message")
        def on_message(message):
            print("Phone got:", message)
            channel.send("Hello back from Phone")

    offer = await signaling.receive()
    if not isinstance(offer, RTCSessionDescription):
        raise RuntimeError("Expected offer first")
    await pc.setRemoteDescription(offer)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    await signaling.send(pc.localDescription)

    async def receive_signaling():
        while True:
            obj = await signaling.receive()
            if isinstance(obj, RTCIceCandidate):
                await pc.addIceCandidate(obj)
            elif obj is None:
                print("Phone: signaling ended")
                break

    signaling_task = asyncio.create_task(receive_signaling())

    await connected_event.wait()
    signaling_task.cancel()

    print("Phone: connected, waiting for channel to open")
    await asyncio.wait_for(channel_open.wait(), timeout=10)

    while pc.connectionState in ("connected", "completed"):
        await asyncio.sleep(1)


async def init_webrtc_connection(ip: str = "127.0.0.1"):
    signaling = TcpSocketSignaling(ip, 8080)
    pc = RTCPeerConnection()

    try:
        await run(pc, signaling)
    except Exception as e:
        print("exception in init webrtc connection: ", str(e))
    finally:
        await pc.close()
        print("End of function - WebRTC PHONE")