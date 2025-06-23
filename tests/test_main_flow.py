from unittest.mock import MagicMock
import main


def test_main_invokes_steps(monkeypatch):
    cfg = {
        'paths': {
            'raw_inputs': 'raw',
            'audio': 'audio',
            'transcriptions': 'trans',
            'metadata': 'meta',
            'templates': 'tpl',
            'outputs': 'out'
        },
        'models': {
            'whisper': 'wh-model',
            'gemini': 'gm-model'
        },
        'prompts': {'summary': 'prompt'},
        'templates': {'default': 'temp.md'}
    }

    monkeypatch.setattr(main, 'load_config', lambda path: cfg)

    called = {}
    monkeypatch.setattr('utilitarios.preparaaudios', MagicMock(side_effect=lambda **k: called.setdefault('prep', k)))
    monkeypatch.setattr('src.ingest.transcribe', MagicMock(side_effect=lambda **k: called.setdefault('trans', k)))
    monkeypatch.setattr('src.process.resumen', MagicMock(side_effect=lambda **k: called.setdefault('proc', k)))
    monkeypatch.setattr('src.deliver.llenado', MagicMock(side_effect=lambda **k: called.setdefault('deliver', k)))

    main.main()

    assert called['prep'] == {'input_dir': 'raw', 'audio_dir': 'audio'}
    assert called['trans'] == {'audio_dir': 'audio', 'output_dir': 'trans', 'model': 'wh-model'}
    assert called['proc']['transcribe_dir'] == 'trans'
    assert called['proc']['metadata_dir'] == 'meta'
    assert called['deliver']['template_dir'] == 'tpl'
    assert called['deliver']['output_dir'] == 'out'
