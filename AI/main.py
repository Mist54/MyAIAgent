from Modules.summarizer.note_handler import save_note, summarize_note
import time

if __name__ == "__main__":
    title = "Summary"
    content = """
    The development of quantum computing has the potential to revolutionize industries ranging from healthcare to finance. Unlike classical computers, which process information in binary (0s and 1s), quantum computers use quantum bits or qubits. These qubits can exist in multiple states simultaneously, thanks to the principles of superposition and entanglement. This unique capability enables quantum computers to perform certain calculations exponentially faster than classical computers.

In healthcare, quantum computing could enable the development of more accurate models for disease prediction and personalized treatments. By processing vast amounts of medical data, quantum computers could uncover new insights into genetic diseases, protein folding, and drug interactions that are currently beyond the reach of classical systems.

In the financial sector, quantum algorithms might be used to optimize investment portfolios, manage risk, and enhance fraud detection. For example, they could solve complex optimization problems that would take classical computers an impractical amount of time to compute. Furthermore, quantum cryptography is a promising field that aims to create ultra-secure encryption methods, which could safeguard sensitive financial data.

Despite the immense potential, the field of quantum computing is still in its early stages. There are several challenges, including the need for more stable qubits and the development of error-correction algorithms. Quantum computers are also incredibly sensitive to their environment, meaning they must be operated at extremely low temperatures, creating additional technological hurdles.

The next few decades will likely see the emergence of hybrid systems, combining classical and quantum computing to solve real-world problems. These systems will leverage the strengths of both approaches and help make quantum computing more accessible and practical for everyday use. However, much work remains before we can fully unlock the power of quantum computing.
    """

    print("=== Testing Regular Summarization ===")
    start_time = time.time()
    # Save note with regular summary
    note_path = save_note(title, content)
    regular_time = time.time() - start_time
    print(f"Note saved at: {note_path}")
    print(f"Time taken: {regular_time:.2f} seconds")

    # Read and print the summary
    print("\nRegular Summary:")
    summary = summarize_note(note_path)
    print(summary)

    print("\n\n=== Testing Key Points Summarization ===")
    start_time = time.time()
    # Save note with key points (3 points)
    key_points_path = save_note(title, content, key_points=3)
    key_points_time = time.time() - start_time
    print(f"Note with key points saved at: {key_points_path}")
    print(f"Time taken: {key_points_time:.2f} seconds")

    # Read and print the key points
    print("\nKey Points Summary:")
    key_points = summarize_note(key_points_path, key_points=3)
    print(key_points)

    print("\n\n=== Testing Key Points Extraction from Existing Note ===")
    start_time = time.time()
    # Extract key points from existing note (5 points)
    extracted_key_points = summarize_note(note_path, key_points=5)
    extraction_time = time.time() - start_time
    print(f"Time taken: {extraction_time:.2f} seconds")
    print("\nExtracted Key Points (5):")
    print(extracted_key_points)

    print("\n\n=== Performance Comparison ===")
    print(f"Regular summarization: {regular_time:.2f} seconds")
    print(f"Key points summarization: {key_points_time:.2f} seconds")
    print(f"Key points extraction: {extraction_time:.2f} seconds")