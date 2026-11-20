
import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;

public class Main extends JFrame {

    private DefaultTableModel model;
    private JTable table;

    private JTextField nameField;
    private JTextField grade1Field;
    private JTextField grade2Field;

    public Main() {
        setTitle("StudentHub - Gestão Acadêmica");
        setSize(800, 500);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        createInterface();
    }

    private void createInterface() {

        JPanel form = new JPanel(new FlowLayout());

        nameField = new JTextField(12);
        grade1Field = new JTextField(5);
        grade2Field = new JTextField(5);

        form.add(new JLabel("Aluno:"));
        form.add(nameField);

        form.add(new JLabel("Nota 1:"));
        form.add(grade1Field);

        form.add(new JLabel("Nota 2:"));
        form.add(grade2Field);

        JButton addButton = new JButton("Cadastrar");
        addButton.addActionListener(e -> addStudent());

        JButton deleteButton = new JButton("Excluir");
        deleteButton.addActionListener(e -> deleteStudent());

        form.add(addButton);
        form.add(deleteButton);

        String[] columns = {
            "Nome", "Média", "Situação"
        };

        model = new DefaultTableModel(columns, 0);
        table = new JTable(model);

        add(form, BorderLayout.NORTH);
        add(new JScrollPane(table), BorderLayout.CENTER);
    }

    private void addStudent() {

        String name = nameField.getText().trim();

        try {
            double grade1 = Double.parseDouble(
                grade1Field.getText().replace(",", ".")
            );

            double grade2 = Double.parseDouble(
                grade2Field.getText().replace(",", ".")
            );

            if (name.isEmpty() ||
                grade1 < 0 || grade1 > 10 ||
                grade2 < 0 || grade2 > 10) {
                throw new IllegalArgumentException();
            }

            Student student = new Student(name, grade1, grade2);

            model.addRow(new Object[]{
                student.getName(),
                String.format("%.2f", student.getAverage()),
                student.getStatus()
            });

            nameField.setText("");
            grade1Field.setText("");
            grade2Field.setText("");

        } catch (IllegalArgumentException ex) {
            JOptionPane.showMessageDialog(
                this,
                "Preencha os dados corretamente. As notas devem estar entre 0 e 10."
            );
        }
    }

    private void deleteStudent() {

        int selected = table.getSelectedRow();

        if (selected == -1) {
            JOptionPane.showMessageDialog(
                this, "Selecione um aluno."
            );
            return;
        }

        model.removeRow(selected);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new Main().setVisible(true);
        });
    }
}
