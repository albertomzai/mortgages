describe('E2E Test for Mortgage Management Dashboard', () => {
  it('should load dashboard, create a mortgage, record a payment and view details', () => {
    // Visit the root page
    cy.visit('/');

    // Verify that the mortgages table is visible
    cy.get('[data-testid="mortgages-table"]').should('be.visible');

    // Click on "Create New Mortgage" button to open modal
    cy.get('[data-testid="create-mortgage-btn"]').click();

    // Fill out the mortgage creation form inside the modal
    cy.get('[data-testid="modal-create"]')
      .within(() => {
        cy.get('[data-testid="client-name-input"]').type('John Doe');
        cy.get('[data-testid="property-address-input"]').type('123 Main St, Springfield');
        cy.get('[data-testid="principal-amount-input"]').type('250000');
        cy.get('[data-testid="interest-rate-input"]').type('3.5');
        cy.get('[data-testid="term-years-input"]').type('30');
        cy.get('[data-testid="start-date-input"]').type('2024-01-01');
        // Submit the form
        cy.get('[data-testid="submit-mortgage-btn"]').click();
      });

    // Wait for the mortgage to be added and appear in the table
    cy.get('[data-testid="mortgages-table"]')
      .contains('John Doe')
      .should('be.visible');

    // Record a payment for the newly created mortgage
    cy.get('[data-testid="mortgage-row-1"]') // assuming first row is the new one
      .within(() => {
        cy.get('[data-testid="record-payment-btn"]').click();
      });

    // Fill out the payment form in modal
    cy.get('[data-testid="modal-record-payment"]')
      .within(() => {
        cy.get('[data-testid="payment-date-input"]').type('2024-02-01');
        cy.get('[data-testid="payment-amount-input"]').type('1000');
        cy.get('[data-testid="submit-payment-btn"]').click();
      });

    // Verify that the balance has been updated in the table
    cy.get('[data-testid="mortgage-row-1"]')
      .contains('$249,000') // example expected new principal after payment
      .should('be.visible');

    // Click on the mortgage row to navigate to detail view
    cy.get('[data-testid="mortgage-row-1"]').click();

    // Verify that the detail view shows the mortgage information
    cy.get('[data-testid="detail-view"]')
      .within(() => {
        cy.contains('John Doe').should('be.visible');
        cy.contains('123 Main St, Springfield').should('be.visible');

        // Verify that amortization plan table is loaded from backend
        cy.get('[data-testid="amortization-table"]').should('be.visible');
        cy.get('[data-testid="amortization-row-1"]')
          .contains('Month 1')
          .and('contain', '$1,000'); // example monthly payment
      });
  });
});