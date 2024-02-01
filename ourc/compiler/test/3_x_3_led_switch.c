/*
    Program
        Turn on/off the led corresponding to the button.
    
    Chip
        # Button(s) with one end at in[0-2] with another end with
        #pull down resister
        [in0-button] [in1-button] [in2-button]
        # Led(s) anode at out[0-2] and cathode at ground with some resister
        [out0-led] [out1-button1] [out2-button2]           
*/
void main() {
    
    int data;
    while(1) {
        INPUT(a);
        OUTPUT(a);
    }
}