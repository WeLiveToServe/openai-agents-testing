
    # Post-record menu
    choice = ui.menu_post_record()
    print(f"User Selection: [{choice}]\n")

    if choice == "1":
        print("gpt-5")
    elif choice == "2":
        print("gpt-4o")
    elif choice == "3":
        print("o3")
    elif choice == "4":
        print("lorum")
    elif choice == "5":
        print("lorum")
    elif choice == "6":
        print("→ Sending to Agent Moneypenny...")
        reply = agents.agent_moneypenny(transcript_raw)

        # Log into .md file
        md_path = session_file + ".md"
        with open(md_path, "a", encoding="utf-8") as f:
            f.write("## Agent Moneypenny\n")
            f.write("### User Transcript\n")
            f.write(transcript_raw.strip() + "\n\n")
            f.write("### Agent Reply\n")
            f.write(reply + "\n")
            f.write("---\n")

        print("✓ Response from Agent Moneypenny:")
        ui.pretty_print_response(reply)
    else:
        print("Invalid choice, please try again.")