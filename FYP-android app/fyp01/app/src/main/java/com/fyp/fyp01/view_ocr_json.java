package com.fyp.fyp01;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.util.Locale;

public class view_ocr_json extends AppCompatActivity {

    TextView view;
    TextToSpeech textToSpeech;
    Button btn;
    int Flag = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_ocr_json);
        Intent i = getIntent();
        final String doc_ocr = i.getStringExtra("JSON_TEXT");
        view = findViewById(R.id.view_text);

        view.setText(doc_ocr);
        btn=(Button)findViewById(R.id.text_to_speech);

        textToSpeech = new TextToSpeech(getApplicationContext(), new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status == TextToSpeech.SUCCESS) {
                    int ttsLang = textToSpeech.setLanguage(Locale.US);

                    if (ttsLang == TextToSpeech.LANG_MISSING_DATA
                            || ttsLang == TextToSpeech.LANG_NOT_SUPPORTED) {
                        Log.e("TTS", "The Language is not supported!");
                    } else {
                        Log.i("TTS", "Language Supported.");
                    }

                    Log.i("TTS", "Initialization success.");
                } else {
                    Toast.makeText(getApplicationContext(), "TTS Initialization failed!", Toast.LENGTH_SHORT).show();
                }
            }

        });

        btn.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View arg0) {
                if(Flag == 0) {
                    String data = doc_ocr;
                    Flag = 1;
                    btn.setText("Stop Text To Speech");
                    int speechStatus = textToSpeech.speak(data, TextToSpeech.QUEUE_FLUSH, null, null);

                    if (speechStatus == TextToSpeech.ERROR) {
                        Log.e("TTS", "Error in converting Text to Speech!");
                    }
                }
                else {
                    Flag = 0;
                    btn.setText("Start Text To Speech");
                    textToSpeech.stop();
                }
            }
        });
    }

}
