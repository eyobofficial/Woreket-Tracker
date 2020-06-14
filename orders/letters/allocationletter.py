from docx.shared import Pt

from shared.letters import LetterTemplate, Receiver, Paragraph, Text
from customers.models import Customer


class AllocationLetter(LetterTemplate):
    """Class for generating allocation letters.

    Attributes:
        receiver: An instance of the Receiver class
        object: An instance of the DeliveryOrder model
    """
    BANK_ACCOUNT = '1000176361038'

    def __init__(self, delivery_order, *args, **kwargs):
        self.receiver = Receiver(
            name='Commercial Bank of Ethiopia',
            department='Trade Service Special Outlet',
            city='Addis Ababa'
        )
        self.object = delivery_order
        super().__init__(self.receiver, *args, **kwargs)

    @property
    def subject(self):
        return f'Documentary Credit Number {self.object.batch.lc_number}'

    def _build_content(self, *args, **kwargs):
        """Builds the letter content."""
        vessel = self.object.vessel
        quantity = self.object.get_allocated_quantity()
        quantity = round(quantity, 2)
        product = self.object.batch.product.name
        category = self.object.batch.product.category.name.lower()
        bol = self.object.bill_of_loading  # bill of loading
        batch = self.object.batch.name
        port = self.object.port.name
        office = self.object.port.office
        arrival_date = self.object.arrival_date
        supplier = self.object.batch.supplier.name
        unit = self.object.unit.code
        eabc = Customer.objects.get(code='EABC')

        greeting = Paragraph(self.document)
        greeting.add_text(Text('Dear Sirs,'))

        p1 = Paragraph(self.document)
        p1.add_texts(
            Text('Reading the subject in caption '),
            Text(vessel, bold=True),
            Text(' a vessel carrying '),
            Text(f'{quantity:,} {unit} {product} {category} ', bold=True),
            Text(f'under B/L {bol} for {batch} ', bold=True),
            Text('will arrive at port of '),
            Text(f'{port} ', bold=True),
            Text('around '),
            Text(f'{arrival_date:%d/%m/%Y}.', bold=True)
        )

        p2 = Paragraph(self.document)
        p2.add_texts(
            Text(
                'On the other hand, we have not yet received original shipping '
                'documents from our supplier '
            ),
            Text(f'{supplier}. ', bold=True),
            Text(
                'Therefore, we hereby request your good office to issue us '
                'delivery order addressing '
            ),
            Text(
                f'{office} and Customs Commissions Addis Ababa Kality Customs '
                'Branch Office and Debit:',
                bold=True
            )
        )

        for allocation in self.object.allocations.all():
            p3 = Paragraph(
                self.document, style='List Bullet',
                line_spacing=1.4, left_indent=Pt(12)
            )
            allocation_quantity = round(allocation.get_total_quantity(), 2)
            if allocation.buyer.code == 'TIG':
                p3.add_texts(
                    Text(
                        f'{eabc} bank account no. '
                        F'{self.BANK_ACCOUNT} for the value of '
                        f'{allocation_quantity:,} {unit} '
                        f'({allocation.buyer.region} Allocation)',
                        bold=True
                    )
                )
            else:
                p3.add_texts(
                    Text(
                        f'{allocation.buyer.name} account for the value of '
                        f'{allocation_quantity:,} {unit} ',
                        bold=True
                    )
                )

        p4 = Paragraph(self.document)
        p4.add_texts(
            Text(
                'For any discrepancies that may occur during the presentation '
                'of these documents, the Ethiopian Agricultural Business '
                'Corporation will undertake the responsibility.'
            )
        )

        p5 = Paragraph(self.document, space_after=Pt(18))
        p5.add_texts(
            Text('Please note that, we authorize you to debit our bank '),
            Text(f'A/C {self.BANK_ACCOUNT} ', bold=True),
            Text(
                'with CBE Addis Ababa branch for any related charge to the '
                'issuance of delivery order.'
            )
        )

        salute = Paragraph(self.document)
        salute.add_text(Text('Sincerely yours,', bold=True))

        # CC
        p6 = Paragraph(self.document, space_before=Pt(60), space_after=Pt(0))
        p6.add_text(Text('C.C:', bold=True))

        p7 = Paragraph(
            self.document, style='List Bullet',
            left_indent=Pt(24), space_before=Pt(0)
        )
        p7.add_text(
            Text('Agricultural Inputs Procurement Department', bold=True)
        )

        p8 = Paragraph(
            self.document, style='List Bullet',
            left_indent=Pt(24), space_after=Pt(0)
        )
        p8.add_text(
            Text('Finance Department', bold=True)
        )

        p9 = Paragraph(self.document, left_indent=Pt(36), space_before=Pt(0))
        p9.add_text(
            Text('AISS', bold=True, underline=True)
        )
