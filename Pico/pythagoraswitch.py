from machine import Pin, PWM, Timer

speaker = PWM(Pin(17, Pin.OUT)) # スピーカーを接続しているGPIO（この例では17番）を作成し、それをPWM()へ渡す
led_onboard = Pin(25, Pin.OUT) # 基板上のLEDを光らせたいのでGPIO25作成

# 使用する音の周波数を宣言しておく。ピタゴラスイッチは低いラ～高いドまでの音を使う
A4 = 440
B4 = 493.883
C5 = 523.251
C5s= 554.365
D5 = 587.330
E5 = 659.255
F5 = 698.456
F5s= 739.989
G5 = 783.991
A5 = 880
B5 = 987.767
C6 = 1046.502

# bps = 6.4 # 原曲128bpm / 60秒 = 2.1333...bps * 3連符 = 6.4bps
mspb = 156 # 6.4bpsの逆数 = 0.156ms　これが8分3連符ひとつ分の音の長さ、音の間隔となる

# ピタゴラスイッチのメロディーを配列で作成。1要素が8分3連符ひとつ分の音の長さになる。0は無音（休符）
melody = [D5,E5,0,D5,E5,0,G5,F5s,0,D5,E5,0,D5,E5,0,D5,E5,0,C6,B5,0,G5,A5,0,D5,E5,0,D5,E5,0,G5,F5s,0,D5,E5,0,B4,A4,0,B4,C5,0,C5s,D5,0,0,D5,0,D5,E5,0,D5,E5,0,G5,F5s,0,D5,E5,0,D5,E5,0,D5,E5,0,C6,B5,0,G5,A5,0,D5,E5,0,D5,E5,0,G5,F5s,0,D5,E5,0,B4,A4,A4,A4,A4,A4,A4,A4,A4,A4,0,0,F5,E5,0,E5,F5s,E5,F5s,G5,G5,G5,D5,0,B4,C5,0,C5,D5,C5s,D5,B4,B4,B4,0,0,D5,E5,0,D5,E5,0,G5,F5s,0,D5,E5,0,D5,E5,0,D5,E5,0,G5,F5s,0,D5,E5,0,D5,E5,0,D5,E5,0,C6,B5,0,0,G5,0,0,0,0,0,0,0,0,0,0,0,0,0,D5,E5,0,D5,E5,0,C6,B5,0,0,G5]
i = 0

# 音を鳴らすためのコールバック関数
def beat(timer):
    global melody
    global led_onboard
    global i
    global speaker
    
    if i >= len(melody): # メロディーを最後まで演奏し終えたら
        speaker.deinit() # スピーカーのPWMを破棄して
        led_onboard.value(0) # LEDを消して
        timer.deinit() # タイマーを破棄して終了
        
    elif int(melody[i]) == 0: # メロディー音が0、つまり無音（休符）の場合
        speaker.duty_u16(0) # PWMのDutyを0とすることで波形は出力されずLOWとなり、音は出ない
        led_onboard.value(0) # LEDを消す
        
    else:
        speaker.freq(int(melody[i])) # PWMの周波数を次のメロディー音の周波数に変更する
        speaker.duty_u16(0x8000) # PWMのDutyを50％に戻し、音を出す。Dutyは0～0xFFFFつまり65535までの間の値で設定
        led_onboard.value(1) # LEDを光らせる

    i += 1 # メロディーを次に進めて終わり

# 8分3連符の間隔でコールバックを呼ぶタイマーを作成し、メロディースタート
tim = Timer()
tim.init(period=mspb, mode=Timer.PERIODIC, callback=beat)
