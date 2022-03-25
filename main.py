import websocket
import _thread
import time
import rel

rel.safe_read()


def on_message(ws, message):
    print(f"You got mail: {message}")


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection sending CONNECT_CONTROLLER")
    ws.send("{\"eventType\" : \"CONNECT_CONTROLLER\",  " +
            "\"data\" : " +
            "{ \"sessionName\" : \"DubbleFF\", " +
            "\"sessionVersion\" : 1, " +
            "\"discardParseErrors\" : false,  " +
            "\"discardEventTypeErrors\" : false, " +
            "\"discardMalformedDataErrors\" : false, " +
            "\"discardInvalidStateErrors\" : false}" +
            "}")


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://keyslam.com:8080",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
