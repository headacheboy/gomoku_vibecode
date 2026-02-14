def main():
    try:
        from .ui import run_ui
    except Exception as e:
        print('Failed to import UI:', e)
        return
    run_ui()


if __name__ == '__main__':
    main()
