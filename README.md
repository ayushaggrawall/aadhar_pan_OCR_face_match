# aadhar_pan_OCR_face_match

Runs a Flask server on the designated port in (app.py)

@app.route("/getface")    : Extracts the face from the document and uploads it to Amazon S3. Returns back the S3 link
@app.route("/getdata")    : OCR data on the pancard/ aadhar card and returns back in dict format.
@app.route("/pandata")    : Testing code explicitly for PANCARD ***
@app.route("/orient")     : Reorients the picture (in readable format) and returns back S3 Link
@app.route('/similarity') : Upload 2 photos. Selfie and ID photo. Returns matching face % between the two images.
