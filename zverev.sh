# Used vietocr / jtessboxeditor to train tesseract:
# 1) first run tiffsplit on zverev.tiff, 
# 2) create a directory and copy a single tiff book page into it
# 3) run jtessboxeditor, 
# 4) select that directory, 
# 5) select make boxes and run, 
# 6) select box editor tab and pick the boxes to train on,
# 7) select train with existing boxes and run,
# 8) copy num.traineddata result to /usr/share/tesseract-ocr/tessdata/

tesseract \
  -c load_system_dawg=false \
  -c load_freq_dawg=false \
  -c tessedit_char_whitelist="0123456789.NF" \
  zverev.tiff zverev -psm 6 -l num
