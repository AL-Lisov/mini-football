with open('raw_bytes.bin', 'rb') as f:
    text = f.read().decode('utf-8', errors='replace')

chunk = text.split('id="request_view_row_')[1]
with open('chunk_sample.html', 'w', encoding='utf-8') as f:
    f.write(chunk[:2000])
